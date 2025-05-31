# Raspberry Pi Pico MicroPython Script for HWIL Testing of pygeomag
import sys
import time
from pygeomag import GeoMag # Assuming pygeomag.py is in the Pico's root or sys.path

# --- Communication Protocol Markers ---
COF_START_MARKER = "COF_START"
COF_END_MARKER = "COF_END"
TEST_PARAMS_MARKER = "TEST_PARAMS:"
RESULTS_MARKER = "RESULTS:"
ERROR_MARKER = "ERROR:"

# --- Global Store for COF Data ---
cof_data_string = None

def read_serial_line():
    """Reads a line from serial input, stripping newline characters."""
    return sys.stdin.readline().strip()

def send_serial_line(line):
    """Sends a line over serial output, adding a newline character."""
    sys.stdout.write(line + '\n')

def run_test_cycle():
    global cof_data_string

    # Phase 1: Receive COF data
    # print("Pico: Waiting for COF data...") # Debug on Pico
    while True:
        line = read_serial_line()
        if line == COF_START_MARKER:
            # print("Pico: COF_START received") # Debug on Pico
            cof_lines = []
            while True:
                cof_line = read_serial_line()
                if cof_line == COF_END_MARKER:
                    # print("Pico: COF_END received") # Debug on Pico
                    cof_data_string = "\n".join(cof_lines)
                    if not cof_data_string:
                        send_serial_line(f"{ERROR_MARKER}Received empty COF data.")
                        cof_data_string = None # Reset to wait for new COF data
                        # print("Pico: Empty COF data, reset.") # Debug
                        break # Break from inner COF reading loop, back to outer COF_START wait
                    # print(f"Pico: COF data stored ({len(cof_data_string)} bytes). Waiting for test params...") # Debug
                    break # Break from inner COF reading loop
                cof_lines.append(cof_line)
            if cof_data_string: # If COF data successfully received and not empty
                break # Break from outer COF_START wait loop, proceed to test params
        elif not line: # Handle potential empty line if host disconnects or sends weird data
            time.sleep_ms(10)


    # Phase 2: Process test parameters
    while True:
        if not cof_data_string: # Should not happen if logic is correct, but as a safeguard
            # print("Pico: ERROR - No COF data, waiting for new COF_START.") # Debug
            # This state means we should go back to waiting for COF_START
            return # Exit this cycle and let main_loop restart it.

        line = read_serial_line()
        if not line: # Handle potential empty line
            time.sleep_ms(10)
            continue

        if line.startswith(TEST_PARAMS_MARKER):
            params_str = line[len(TEST_PARAMS_MARKER):]
            try:
                # print(f"Pico: Received params: {params_str}") # Debug
                parts = params_str.split(',')
                if len(parts) != 4:
                    send_serial_line(f"{ERROR_MARKER}Invalid number of test parameters. Expected 4, got {len(parts)}")
                    continue

                time_val = float(parts[0])
                alt_km = float(parts[1]) # Height in km
                glat = float(parts[2])
                glon = float(parts[3])

                # Initialize GeoMag with the stored COF string
                # Assuming pygeomag.py handles the high_resolution flag internally based on COF.
                # If not, that might be an enhancement if test files distinguish this.
                gm = GeoMag(coefficients_data=cof_data_string)

                result = gm.calculate(glat=glat, glon=glon, alt=alt_km, time=time_val)

                # Extract results
                # Format: D,I,H,X,Y,Z,F with fixed precision (e.g., 5 decimal places for angles, 2 for nT)
                # This precision should match what the host expects or can tolerate.
                results_str = (
                    f"{result.d:.5f},{result.i:.5f},"
                    f"{result.h:.2f},{result.x:.2f},{result.y:.2f},{result.z:.2f},{result.f:.2f}"
                )
                send_serial_line(f"{RESULTS_MARKER}{results_str}")
                # print(f"Pico: Sent results: {results_str}") # Debug

            except Exception as e:
                # print(f"Pico: Error during calculation: {e}") # Debug
                send_serial_line(f"{ERROR_MARKER}Calculation error: {str(e)}")

        elif line == COF_START_MARKER:
            # Host wants to send new COF data, break from test param loop and restart cycle
            # print("Pico: COF_START received during test phase. Restarting cycle.") # Debug
            cof_data_string = None # Clear old COF data
            # Re-enter the COF reading logic by letting run_test_cycle be called again
            # To do this, we effectively prepend the COF_START_MARKER back to an imaginary input stream
            # or simply return and let the outer loop handle it by restarting.
            # For simplicity here, we'll return and let main_loop re-initiate.
            return


def main_loop():
    """Main loop to handle COF data and test parameters."""
    global cof_data_string
    while True:
        cof_data_string = None # Ensure cof_data is reset for each new session/COF load
        # print("Pico: Top of main_loop, cof_data_string reset.") # Debug
        run_test_cycle()

if __name__ == "__main__":
    # Small delay to allow serial connection to establish if needed,
    # though for USB serial it's usually instant.
    time.sleep_ms(100)
    main_loop()
