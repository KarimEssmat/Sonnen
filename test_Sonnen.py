import pytest


class DUT:
    def __init__(self):
        self.pv_power = 0
        self.house_consumption = 0
        self.battery_power = 0
        self.grid_power = 0
        self.inverter_max_power = 5000
        self.battery_max_power = 5000

    def set(self, key: str, value) -> bool:
        if hasattr(self, key):
            setattr(self, key, value)
            return True
        return False

    def get(self, key: str) -> str:
        return str(getattr(self, key, 0))


@pytest.fixture
def dut():

    dut_device = DUT()
    yield dut_device
    # Reset DUT state after the test
    dut_device.set('pv_power', 0)
    dut_device.set('house_consumption', 0)
    dut_device.set('battery_power', 0)
    dut_device.set('grid_power', 0)


def fibonacci_generator():
    """Generator for Fibonacci sequence."""
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b


# Test Cases

def test_basic_setup(dut):
    """Basic system setup: 1 inverter, up to 2 battery modules."""
    fib_gen = fibonacci_generator()
    pv_power = next(fib_gen)
    house_consumption = next(fib_gen)

    dut.set('pv_power', pv_power)
    dut.set('house_consumption', house_consumption)
    dut.set('inverter_max_power', 2000)
    dut.set('battery_max_power', 2000)

    surplus = dut.pv_power - dut.house_consumption
    if surplus > 0:
        battery_charge = min(surplus, dut.battery_max_power)
        dut.set('battery_power', battery_charge)
        grid_export = surplus - battery_charge
        dut.set('grid_power', grid_export)
    else:
        deficit = abs(surplus)
        battery_discharge = min(deficit, dut.battery_max_power)
        dut.set('battery_power', -battery_discharge)
        grid_import = deficit - battery_discharge
        dut.set('grid_power', grid_import)

    assert int(dut.get('battery_power')) == max(0, min(pv_power - house_consumption, 2000))
    assert int(dut.get('grid_power')) == max(0, surplus - dut.battery_max_power)


def test_standard_setup(dut):
    """Standard system setup: 1 inverter, up to 3 battery modules."""
    fib_gen = fibonacci_generator()
    pv_power = next(fib_gen)
    house_consumption = next(fib_gen)

    dut.set('pv_power', pv_power)
    dut.set('house_consumption', house_consumption)
    dut.set('inverter_max_power', 3000)
    dut.set('battery_max_power', 3000)

    surplus = dut.pv_power - dut.house_consumption
    if surplus > 0:
        battery_charge = min(surplus, dut.battery_max_power)
        dut.set('battery_power', battery_charge)
        grid_export = surplus - battery_charge
        dut.set('grid_power', grid_export)
    else:
        deficit = abs(surplus)
        battery_discharge = min(deficit, dut.battery_max_power)
        dut.set('battery_power', -battery_discharge)
        grid_import = deficit - battery_discharge
        dut.set('grid_power', grid_import)

    assert int(dut.get('battery_power')) == max(0, min(pv_power - house_consumption, 3000))
    assert int(dut.get('grid_power')) == max(0, surplus - dut.battery_max_power)


def test_pro_setup(dut):
    """Pro system setup: 1 inverter, up to 5 battery modules."""
    fib_gen = fibonacci_generator()
    pv_power = next(fib_gen)
    house_consumption = next(fib_gen)

    dut.set('pv_power', pv_power)
    dut.set('house_consumption', house_consumption)
    dut.set('inverter_max_power', 5000)
    dut.set('battery_max_power', 5000)

    surplus = dut.pv_power - dut.house_consumption
    if surplus > 0:
        battery_charge = min(surplus, dut.battery_max_power)
        dut.set('battery_power', battery_charge)
        grid_export = surplus - battery_charge
        dut.set('grid_power', grid_export)
    else:
        deficit = abs(surplus)
        battery_discharge = min(deficit, dut.battery_max_power)
        dut.set('battery_power', -battery_discharge)
        grid_import = deficit - battery_discharge
        dut.set('grid_power', grid_import)

    assert int(dut.get('battery_power')) == max(0, min(pv_power - house_consumption, 5000))
    assert int(dut.get('grid_power')) == max(0, surplus - dut.battery_max_power)


def test_zero_pv_power(dut):
    """Zero PV power: no solar energy available."""
    dut.set('pv_power', 0)
    dut.set('house_consumption', 3000)
    dut.set('battery_max_power', 2000)

    deficit = dut.house_consumption - dut.pv_power
    battery_discharge = min(deficit, dut.battery_max_power)
    dut.set('battery_power', -battery_discharge)
    grid_import = deficit - battery_discharge
    dut.set('grid_power', grid_import)

    assert int(dut.get('battery_power')) == -2000
    assert int(dut.get('grid_power')) == 1000


def test_equal_pv_and_house_consumption(dut):
    """Equal PV production and house consumption: no surplus or deficit."""
    fib_gen = fibonacci_generator()
    value = next(fib_gen)

    dut.set('pv_power', value)
    dut.set('house_consumption', value)

    surplus = dut.pv_power - dut.house_consumption
    dut.set('battery_power', surplus)
    dut.set('grid_power', 0)

    assert int(dut.get('battery_power')) == 0
    assert int(dut.get('grid_power')) == 0


def test_high_pv_power(dut):
    """High PV power: PV power much greater than house consumption."""
    fib_gen = fibonacci_generator()
    pv_power = next(fib_gen) * 1000
    house_consumption = next(fib_gen)

    dut.set('pv_power', pv_power)
    dut.set('house_consumption', house_consumption)
    dut.set('battery_max_power', 5000)

    surplus = dut.pv_power - dut.house_consumption
    battery_charge = min(surplus, dut.battery_max_power)
    dut.set('battery_power', battery_charge)
    grid_export = surplus - battery_charge
    dut.set('grid_power', grid_export)

    assert int(dut.get('battery_power')) == min(pv_power - house_consumption, dut.battery_max_power)
    assert int(dut.get('grid_power')) == max(0, surplus - dut.battery_max_power)


if __name__ == "__main__":
    pytest.main()



#                        Advantages of Using pytest Fixtures over Setup and Teardown Methods


# Modularity: Pytest fixtures allow for better code reuse and modular test setup.
# Each fixture can be created separately and used across multiple test cases.
#
# Cleaner Tests: With fixtures, the setup and teardown logic is separated from
# the actual test code, making tests cleaner and easier to understand.
#
# Scope and Auto use: Fixtures in pytest can be scoped to function, class, module,
# or session levels. You can also automatically apply a fixture to multiple tests
# without explicitly passing it.
#
# Ease of Cleanup: Pytest fixtures can include finalization logic to clean up
# resources after the test finishes, ensuring a clean state without needing
# explicit teardown methods.



#                   Integrating Machine Learning in a Hardware-Dependent Test Automation Framework


# Integrating Machine Learning (ML) into a hardware-dependent test automation
# framework could improve test predictions, anomaly detection, and resource optimization.
# Here’s how it could be done:
#
# Anomaly Detection: Use ML models to predict the expected behavior of the system
# and flag anomalies during testing. For example, if the system is supposed to charge
# the battery with 200W from the PV, ML can detect if the actual behavior deviates
# from this prediction.
#
# Predictive Maintenance: ML can be used to predict when certain components (e.g.,
# battery, inverter) might fail based on usage patterns and historical data.
# This helps to automate the maintenance scheduling of hardware.
#
# Optimization: ML algorithms can optimize power consumption and distribution
# patterns based on real-time data, helping to better simulate different energy
# management scenarios in the test automation process.
#
# Data-Driven Decisions: Use historical test data to train models that predict
# which configurations and conditions will result in the most reliable performance.
# These models can be used to automatically generate test cases or refine the testing process.
