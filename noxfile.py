import nox


@nox.session
def tests(session):
    session.install("pytest", "aiohttp")
    session.run("pytest", "tests", "-v")