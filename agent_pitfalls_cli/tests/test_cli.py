"""CLI 子命令集成测试。"""

import json

from agent_pitfalls_cli.cli import main


class TestCLI:
    def test_version(self, capsys):
        ret = main(["--version"])
        assert ret == 0
        out = capsys.readouterr().out
        assert "0.1.0" in out

    def test_help(self, capsys):
        ret = main(["--help"])
        assert ret == 0
        out = capsys.readouterr().out
        assert "agent-pitfalls" in out

    def test_build(self, capsys):
        ret = main(["build"])
        assert ret == 0

    def test_search_human(self, capsys):
        ret = main(["search", "context overflow", "--no-color", "-n", "2"])
        assert ret == 0
        out = capsys.readouterr().out
        assert "matches" in out

    def test_search_json(self, capsys):
        ret = main(["search", "context overflow", "--json", "-n", "1"])
        assert ret == 0
        out = capsys.readouterr().out
        data = json.loads(out)
        assert "hits" in data
        assert len(data["hits"]) >= 1

    def test_list(self, capsys):
        ret = main(["list", "--no-color", "-n", "3"])
        assert ret == 0
        out = capsys.readouterr().out
        assert len(out.strip().splitlines()) >= 1

    def test_platforms(self, capsys):
        ret = main(["platforms", "--no-color"])
        assert ret == 0
        out = capsys.readouterr().out
        assert "generic" in out

    def test_categories(self, capsys):
        ret = main(["categories", "--no-color"])
        assert ret == 0
        out = capsys.readouterr().out
        assert "security" in out
