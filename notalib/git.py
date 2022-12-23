from typing import Optional, Sequence
from dataclasses import dataclass
from subprocess import run


SHORT_HASH_LENGTH = 7


@dataclass(frozen=True)
class HashableData:
	hash: str

	@property
	def short_hash(self) -> str:
		return self.hash[:SHORT_HASH_LENGTH]


@dataclass(frozen=True)
class Tag(HashableData):
	label: str


@dataclass(frozen=True)
class Commit(HashableData):
	short_description: str


def get_current_commit() -> Optional[Commit]:
	"""
	Returns last commit data if called inside git repo.
	"""
	commit_data = _run_git_command_safely(('log', '-1', '--pretty=%H %s'))

	if commit_data:
		commit_data = commit_data.split()
		hash, short_description = commit_data[0], ' '.join(commit_data[1:])
		return Commit(short_description=short_description, hash=hash)

	return None


def get_last_tag() -> Optional[Tag]:
	"""
	Returns last tag data if called inside git repo.
	"""
	last_tag = _run_git_command_safely(('describe', '--abbrev=0', '--tags'))

	if last_tag:
		hash = get_tag_hash(last_tag)

		if hash:
			return Tag(label=last_tag, hash=hash)

	return None


def get_tag_hash(tag: str) -> Optional[str]:
	"""
	Returns hash of specified tag if it exists and function is called inside git repo.
	"""
	command_stdout = _run_git_command_safely(('show-ref', tag))

	if command_stdout:
		return command_stdout.split()[0]

	return None


def _run_git_command_safely(command_args: Sequence[str]) -> Optional[str]:
	"""
	Executes the git command with the specified arguments.

	Returns:
		None in case of an error otherwise stdout.
	"""
	completed_process = run(['git', *command_args], capture_output=True)

	if completed_process.returncode != 0:
		return None

	return completed_process.stdout.decode(encoding='utf-8').strip()
