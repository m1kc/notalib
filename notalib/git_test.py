from notalib.git import (
	HashableData, Tag, Commit, get_current_commit, get_last_tag, get_tag_hash, _run_git_command_safely,
	SHORT_HASH_LENGTH,
)
from notalib.test_fakes import FakeFunction

from unittest.mock import patch


class FakeGit(FakeFunction):
	def __init__(self, return_value = None):
		super().__init__(return_value or [None])

	def __call__(self, *args, **kwargs):
		result = super().__call__(*args, **kwargs)
		return result[self.call_count - 1]


class CapturedProcessStub:
	def __init__(self, returncode: int = 0, stdout: bytes = b''):
		self.returncode = returncode
		self.stdout = stdout


class FakeSubprocessRun(FakeFunction):
	def __init__(self, return_value: CapturedProcessStub = CapturedProcessStub()):
		super().__init__(return_value)


class TestHashableData:
	def test___init__(self):
		assert HashableData(hash="1234567890").hash == "1234567890"

	def test_short_hash(self):
		assert HashableData(hash="1234567890").short_hash == "1234567890"[:SHORT_HASH_LENGTH]


class TestTag:
	def test___init__(self):
		tag = Tag(label="label", hash="hash")
		assert tag.label == "label"
		assert tag.hash == "hash"


class TestCommit:
	def test___init__(self):
		commit = Commit(short_description="Description", hash="hash")
		assert commit.short_description == "Description"
		assert commit.hash == "hash"


def test_get_current_commit():
	fake_git = FakeGit()

	with patch("notalib.git._run_git_command_safely", new=fake_git):
		assert get_current_commit() is None
		assert fake_git.call_count == 1
		assert fake_git.last_call_args == (('log', '-1', '--pretty=%H %s'), )

	fake_git = FakeGit(return_value=["hash Commit message"])
	with patch("notalib.git._run_git_command_safely", new=fake_git):
		commit = get_current_commit()
		assert commit.hash == "hash"
		assert commit.short_description == "Commit message"
		assert fake_git.call_count == 1


def test_get_tag_hash():
	fake_git = FakeGit()

	with patch("notalib.git._run_git_command_safely", new=fake_git):
		assert get_tag_hash("tag") is None
		assert fake_git.call_count == 1
		assert fake_git.last_call_args == (('show-ref', 'tag'), )

	fake_git = FakeGit(return_value=["hashhashhash"])
	with patch("notalib.git._run_git_command_safely", new=fake_git):
		tag_hash = get_tag_hash("v2.2.0")
		assert tag_hash == "hashhashhash"
		assert fake_git.call_count == 1


def test_get_last_tag():
	fake_git = FakeGit()

	with patch("notalib.git._run_git_command_safely", new=fake_git):
		assert get_last_tag() is None
		assert fake_git.call_count == 1
		assert fake_git.last_call_args == (('describe', '--abbrev=0', '--tags'), )

	fake_git = FakeGit(return_value=["v2.2.0", "hashhashhash"])
	with patch("notalib.git._run_git_command_safely", new=fake_git):
		tag = get_last_tag()
		assert tag.hash == "hashhashhash"
		assert tag.label == "v2.2.0"
		assert fake_git.call_count == 2


def test__run_git_command_safely():
	fake_run = FakeSubprocessRun()

	with patch("notalib.git.run", new=fake_run):
		assert _run_git_command_safely([]) == ""
		assert fake_run.call_count == 1
		assert fake_run.last_call_args == (['git'], )
		assert fake_run.last_call_kwargs == {'capture_output': True}

		fake_run.return_value.stdout = "hello world".encode()
		assert _run_git_command_safely([]) == "hello world"
		assert fake_run.call_count == 2

		fake_run.return_value.returncode = 1
		assert _run_git_command_safely(['arg1', 'arg2']) is None
		assert fake_run.call_count == 3
		assert fake_run.last_call_args == (['git', 'arg1', 'arg2'], )
		assert fake_run.last_call_kwargs == {'capture_output': True}
