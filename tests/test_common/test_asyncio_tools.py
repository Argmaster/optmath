from optmath.common.asyncio_tools import await_async


def test_await_async():
    async def function(a):
        assert a == 0x44
        return 0x33

    assert await_async(function(0x44)) == 0x33
