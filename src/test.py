import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles
from encoder import Encoder

clocks_per_phase = 10

async def run_encoder_test(encoder, max_count):
    for i in range(clocks_per_phase * 2 * max_count):
        await encoder.update(1)

    # let noisy transition finish, otherwise can get an extra count
    for i in range(10):
        await encoder.update(0)

@cocotb.test()
async def test_rgb_mixer(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # reset
    dut._log.info("reset")
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    encoder0 = Encoder(dut.clk, dut.enc0_a, dut.enc0_b, clocks_per_phase = clocks_per_phase, noise_cycles = clocks_per_phase / 4)
    encoder1 = Encoder(dut.clk, dut.enc1_a, dut.enc1_b, clocks_per_phase = clocks_per_phase, noise_cycles = clocks_per_phase / 4)
    encoder2 = Encoder(dut.clk, dut.enc2_a, dut.enc2_b, clocks_per_phase = clocks_per_phase, noise_cycles = clocks_per_phase / 4)

    # pwm should all be low at start
    assert dut.pwm0_out == 0
    assert dut.pwm1_out == 0
    assert dut.pwm2_out == 0

    # do 3 ramps for each encoder 
    max_count = 255
    await run_encoder_test(encoder0, max_count)
    await run_encoder_test(encoder1, max_count)
    await run_encoder_test(encoder2, max_count)

    # sync to pwm
    await RisingEdge(dut.pwm0_out)
    await FallingEdge(dut.clk)
    # pwm should all be on for max_count 
    for i in range(max_count): 
        assert dut.pwm0_out == 1
        assert dut.pwm1_out == 1
        assert dut.pwm2_out == 1
        await ClockCycles(dut.clk, 1)
