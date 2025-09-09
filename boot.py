"""
Boot configuration for NeoPixel Picture Frame
Sets system optimizations for maximum performance
"""
import microcontroller
import storage
import gc
from matrix_modules.constants import TARGET_CPU_FREQUENCY

# Overclock the RP2350 for maximum performance
# Safe overclocking range: 150MHz (default) to 300MHz
# We'll use 266MHz for a good balance of speed and stability
try:
    # Set CPU frequency using constant
    microcontroller.cpu.frequency = TARGET_CPU_FREQUENCY
    print(f"Boot: CPU overclocked to {microcontroller.cpu.frequency / 1_000_000:.0f} MHz")
except Exception as e:
    print(f"Boot: Overclock failed - {e}")
    pass

# Optimize garbage collection
gc.collect()
gc.threshold(8192)  # Set GC threshold for better performance

# Make filesystem read-only for better performance (optional)
# Uncomment if you don't need to write files during runtime
# storage.remount("/", readonly=True)