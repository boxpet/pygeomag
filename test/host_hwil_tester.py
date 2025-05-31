# Host PC Python Script for HWIL Testing of pygeomag on Raspberry Pi Pico
import argparse
import sys
import time
import serial

# --- Communication Protocol Markers (should match Pico script) ---
COF_START_MARKER = "COF_START"
COF_END_MARKER = "COF_END"
TEST_PARAMS_MARKER = "TEST_PARAMS:"
RESULTS_MARKER = "RESULTS:"
ERROR_MARKER = "ERROR:"

# --- Default Configuration ---
DEFAULT_BAUD_RATE = 115200
# Tolerances for comparison (adjust as needed)
# Based on WMM2020_TEST_VALUES.txt: angles mostly .2f, nT mostly .1f
TOLERANCES = {
    'D': 0.015,  # Declination (degrees)
    'I': 0.015,  # Inclination (degrees)
    'H': 0.15,   # Horizontal Intensity (nT)
    'X': 0.15,   # North Component (nT)
    'Y': 0.15,   # East Component (nT)
    'Z': 0.15,   # Vertical Component (nT)
    'F': 0.15    # Total Intensity (nT)
}
# Indices for parsing test file lines (0-indexed)
# Field 1: Date -> 0
# Field 2: Height -> 1
# Field 3: Lat -> 2
# Field 4: Lon -> 3
# Field 5: D -> 4
# Field 6: I -> 5
# Field 7: H -> 6
# Field 8: X -> 7
# Field 9: Y -> 8
# Field 10: Z -> 9
# Field 11: F -> 10
TEST_FILE_INDICES = {
    'date': 0, 'alt': 1, 'lat': 2, 'lon': 3,
    'D': 4, 'I': 5, 'H': 6, 'X': 7, 'Y': 8, 'Z': 9, 'F': 10
}
RESULT_FIELDS = ['D', 'I', 'H', 'X', 'Y', 'Z', 'F']


def send_command(ser, command_str):
    """Sends a command to the Pico, adding a newline."""
    # print(f"Host: Sending: {command_str}") # Debug
    ser.write(command_str.encode('utf-8') + b'\n')
    ser.flush() # Ensure data is sent immediately

def receive_response(ser, timeout_seconds=5.0):
    """Receives a response line from the Pico."""
    start_time = time.time()
    while True:
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').strip()
            # print(f"Host: Received: {response}") # Debug
            return response
        if time.time() - start_time > timeout_seconds:
            print("Host: Timeout waiting for response from Pico.")
            return None
        time.sleep(0.01) # Small delay to avoid busy-waiting

def send_cof_data(ser, cof_file_path):
    """Reads a COF file and sends its content to the Pico."""
    print(f"Host: Reading COF file: {cof_file_path}")
    try:
        with open(cof_file_path, 'r') as f:
            cof_content = f.read()
    except FileNotFoundError:
        print(f"Host: ERROR - COF file not found: {cof_file_path}")
        return False

    print("Host: Sending COF data to Pico...")
    send_command(ser, COF_START_MARKER)

    for line in cof_content.splitlines():
        send_command(ser, line) # Send each line of the COF file
        # time.sleep(0.001) # Small delay if Pico has trouble with rapid lines

    send_command(ser, COF_END_MARKER)

    # It might be good to wait for an acknowledgement or check for errors from Pico
    # For now, assume Pico handles it or will report error on next command if COF load failed.
    # A simple check:
    response = receive_response(ser, timeout_seconds=2.0)
    if response and response.startswith(ERROR_MARKER):
        print(f"Host: Pico reported an error after sending COF data: {response}")
        return False
    elif response: # Pico might send something else, or nothing if it's just waiting
        print(f"Host: Pico response after COF_END (unexpected, ignoring): {response}")

    print("Host: COF data sent.")
    return True


def run_tests(ser, test_values_file_path):
    """Parses test values, sends them to Pico, and verifies results."""
    print(f"Host: Reading test values from: {test_values_file_path}")
    try:
        with open(test_values_file_path, 'r') as f:
            test_lines = f.readlines()
    except FileNotFoundError:
        print(f"Host: ERROR - Test values file not found: {test_values_file_path}")
        return 0, 0, 0 # total, passed, failed

    test_cases = []
    for line_num, line in enumerate(test_lines):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        parts = line.split()
        if len(parts) < max(TEST_FILE_INDICES.values()) + 1: # Ensure enough parts for all needed fields
            print(f"Host: Warning - Skipping malformed line {line_num+1} in test file: {line}")
            continue
        test_cases.append(parts)

    num_total_tests = len(test_cases)
    num_passed = 0
    num_failed = 0

    print(f"Host: Starting {num_total_tests} tests...")

    for i, test_case_parts in enumerate(test_cases):
        date = float(test_case_parts[TEST_FILE_INDICES['date']])
        alt_km = float(test_case_parts[TEST_FILE_INDICES['alt']]) # Height in km
        glat = float(test_case_parts[TEST_FILE_INDICES['lat']])
        glon = float(test_case_parts[TEST_FILE_INDICES['lon']])

        expected_results = {}
        for field_name in RESULT_FIELDS:
            expected_results[field_name] = float(test_case_parts[TEST_FILE_INDICES[field_name]])

        params_str = f"{date},{alt_km},{glat},{glon}"
        send_command(ser, f"{TEST_PARAMS_MARKER}{params_str}")

        response = receive_response(ser)

        if response is None:
            print(f"Host: Test {i+1}/{num_total_tests} FAILED (Timeout)")
            num_failed += 1
            continue

        if response.startswith(ERROR_MARKER):
            print(f"Host: Test {i+1}/{num_total_tests} FAILED (Pico Error: {response[len(ERROR_MARKER):]})")
            print(f"      Input Params: Date={date}, Alt={alt_km}km, Lat={glat}, Lon={glon}")
            num_failed += 1
            continue

        if not response.startswith(RESULTS_MARKER):
            print(f"Host: Test {i+1}/{num_total_tests} FAILED (Unexpected response: {response})")
            num_failed += 1
            continue

        pico_results_str = response[len(RESULTS_MARKER):]
        pico_results_parts = pico_results_str.split(',')

        if len(pico_results_parts) != len(RESULT_FIELDS):
            print(f"Host: Test {i+1}/{num_total_tests} FAILED (Malformed result from Pico: {pico_results_str})")
            num_failed += 1
            continue

        pico_results_float = {}
        try:
            for j, field_name in enumerate(RESULT_FIELDS):
                pico_results_float[field_name] = float(pico_results_parts[j])
        except ValueError:
            print(f"Host: Test {i+1}/{num_total_tests} FAILED (Non-float value in Pico results: {pico_results_parts})")
            num_failed += 1
            continue

        test_passed_locally = True
        fail_details = []
        for field_name in RESULT_FIELDS:
            expected = expected_results[field_name]
            pico_val = pico_results_float[field_name]
            tolerance = TOLERANCES[field_name]

            if abs(pico_val - expected) > tolerance:
                test_passed_locally = False
                fail_details.append(f"{field_name}: Pico={pico_val:.4f}, Exp={expected:.4f}, Diff={pico_val - expected:.4f}, Tol={tolerance:.4f}")

        if test_passed_locally:
            print(f"Host: Test {i+1}/{num_total_tests} PASSED")
            num_passed += 1
        else:
            print(f"Host: Test {i+1}/{num_total_tests} FAILED")
            print(f"      Input Params: Date={date}, Alt={alt_km}km, Lat={glat}, Lon={glon}")
            for detail in fail_details:
                print(f"      - {detail}")
            num_failed += 1

        time.sleep(0.05) # Small delay between tests

    return num_total_tests, num_passed, num_failed


def main():
    parser = argparse.ArgumentParser(description="HWIL Test Host for pygeomag on Raspberry Pi Pico.")
    parser.add_argument("serial_port", help="Serial port connected to the Pico (e.g., /dev/ttyACM0 or COM3)")
    parser.add_argument("--baud_rate", type=int, default=DEFAULT_BAUD_RATE, help="Serial baud rate")
    parser.add_argument("--cof_file", required=True, help="Path to the WMM.COF file (e.g., ../pygeomag/wmm/WMM_2020.COF)")
    parser.add_argument("--test_file", required=True, help="Path to the test values file (e.g., WMM2020_TEST_VALUES.txt)")

    args = parser.parse_args()

    print(f"Host: Connecting to Pico on {args.serial_port} at {args.baud_rate} baud...")
    try:
        # ser = serial.Serial(args.serial_port, args.baud_rate, timeout=1) # timeout for readline
        # Using a shorter timeout for individual readline, and longer in receive_response
        ser = serial.Serial(args.serial_port, args.baud_rate, timeout=0.1)
    except serial.SerialException as e:
        print(f"Host: ERROR - Could not open serial port {args.serial_port}: {e}")
        sys.exit(1)

    time.sleep(2) # Wait for Pico to initialize/serial connection to stabilize

    if not send_cof_data(ser, args.cof_file):
        print("Host: Failed to send COF data to Pico. Exiting.")
        ser.close()
        sys.exit(1)

    # Brief pause after sending COF data for Pico to process it, if needed.
    # The Pico script is designed to process COF then wait for test params.
    print("Host: Waiting a moment for Pico to process COF data...")
    time.sleep(1)

    total_tests, passed_tests, failed_tests = run_tests(ser, args.test_file)

    print("\n--- HWIL Test Summary ---")
    print(f"Total tests run: {total_tests}")
    print(f"Tests PASSED:    {passed_tests}")
    print(f"Tests FAILED:    {failed_tests}")
    print("-------------------------")

    ser.close()
    print("Host: Serial connection closed.")

    if failed_tests > 0:
        sys.exit(1) # Exit with error code if any tests failed
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
