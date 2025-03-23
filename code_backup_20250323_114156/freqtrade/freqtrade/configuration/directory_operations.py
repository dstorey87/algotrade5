import logging
# REMOVED_UNUSED_CODE: import shutil
# REMOVED_UNUSED_CODE: from pathlib import Path

# REMOVED_UNUSED_CODE: from freqtrade.configuration.detect_environment import running_in_docker
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.constants import (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     USER_DATA_FILES,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     USERPATH_FREQAIMODELS,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     USERPATH_HYPEROPTS,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     USERPATH_NOTEBOOKS,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     USERPATH_STRATEGIES,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     Config,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: )
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def create_datadir(config: Config, datadir: str | None = None) -> Path:
# REMOVED_UNUSED_CODE:     folder = Path(datadir) if datadir else Path(f"{config['user_data_dir']}/data")
# REMOVED_UNUSED_CODE:     if not datadir:
# REMOVED_UNUSED_CODE:         # set datadir
# REMOVED_UNUSED_CODE:         exchange_name = config.get("exchange", {}).get("name", "").lower()
# REMOVED_UNUSED_CODE:         folder = folder.joinpath(exchange_name)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if not folder.is_dir():
# REMOVED_UNUSED_CODE:         folder.mkdir(parents=True)
# REMOVED_UNUSED_CODE:         logger.info(f"Created data directory: {datadir}")
# REMOVED_UNUSED_CODE:     return folder


# REMOVED_UNUSED_CODE: def chown_user_directory(directory: Path) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Use Sudo to change permissions of the home-directory if necessary
# REMOVED_UNUSED_CODE:     Only applies when running in docker!
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if running_in_docker():
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             import subprocess  # noqa: S404
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             subprocess.check_output(["sudo", "chown", "-R", "ftuser:", str(directory.resolve())])
# REMOVED_UNUSED_CODE:         except Exception:
# REMOVED_UNUSED_CODE:             logger.warning(f"Could not chown {directory}")


# REMOVED_UNUSED_CODE: def create_userdata_dir(directory: str, create_dir: bool = False) -> Path:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Create userdata directory structure.
# REMOVED_UNUSED_CODE:     if create_dir is True, then the parent-directory will be created if it does not exist.
# REMOVED_UNUSED_CODE:     Sub-directories will always be created if the parent directory exists.
# REMOVED_UNUSED_CODE:     Raises OperationalException if given a non-existing directory.
# REMOVED_UNUSED_CODE:     :param directory: Directory to check
# REMOVED_UNUSED_CODE:     :param create_dir: Create directory if it does not exist.
# REMOVED_UNUSED_CODE:     :return: Path object containing the directory
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     sub_dirs = [
# REMOVED_UNUSED_CODE:         "backtest_results",
# REMOVED_UNUSED_CODE:         "data",
# REMOVED_UNUSED_CODE:         USERPATH_HYPEROPTS,
# REMOVED_UNUSED_CODE:         "hyperopt_results",
# REMOVED_UNUSED_CODE:         "logs",
# REMOVED_UNUSED_CODE:         USERPATH_NOTEBOOKS,
# REMOVED_UNUSED_CODE:         "plot",
# REMOVED_UNUSED_CODE:         USERPATH_STRATEGIES,
# REMOVED_UNUSED_CODE:         USERPATH_FREQAIMODELS,
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE:     folder = Path(directory)
# REMOVED_UNUSED_CODE:     chown_user_directory(folder)
# REMOVED_UNUSED_CODE:     if not folder.is_dir():
# REMOVED_UNUSED_CODE:         if create_dir:
# REMOVED_UNUSED_CODE:             folder.mkdir(parents=True)
# REMOVED_UNUSED_CODE:             logger.info(f"Created user-data directory: {folder}")
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 f"Directory `{folder}` does not exist. "
# REMOVED_UNUSED_CODE:                 "Please use `freqtrade create-userdir` to create a user directory"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Create required subdirectories
# REMOVED_UNUSED_CODE:     for f in sub_dirs:
# REMOVED_UNUSED_CODE:         subfolder = folder / f
# REMOVED_UNUSED_CODE:         if not subfolder.is_dir():
# REMOVED_UNUSED_CODE:             if subfolder.exists() or subfolder.is_symlink():
# REMOVED_UNUSED_CODE:                 raise OperationalException(
# REMOVED_UNUSED_CODE:                     f"File `{subfolder}` exists already and is not a directory. "
# REMOVED_UNUSED_CODE:                     "Freqtrade requires this to be a directory."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             subfolder.mkdir(parents=False)
# REMOVED_UNUSED_CODE:     return folder


# REMOVED_UNUSED_CODE: def copy_sample_files(directory: Path, overwrite: bool = False) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Copy files from templates to User data directory.
# REMOVED_UNUSED_CODE:     :param directory: Directory to copy data to
# REMOVED_UNUSED_CODE:     :param overwrite: Overwrite existing sample files
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     if not directory.is_dir():
# REMOVED_UNUSED_CODE:         raise OperationalException(f"Directory `{directory}` does not exist.")
# REMOVED_UNUSED_CODE:     sourcedir = Path(__file__).parents[1] / "templates"
# REMOVED_UNUSED_CODE:     for source, target in USER_DATA_FILES.items():
# REMOVED_UNUSED_CODE:         targetdir = directory / target
# REMOVED_UNUSED_CODE:         if not targetdir.is_dir():
# REMOVED_UNUSED_CODE:             raise OperationalException(f"Directory `{targetdir}` does not exist.")
# REMOVED_UNUSED_CODE:         targetfile = targetdir / source
# REMOVED_UNUSED_CODE:         if targetfile.exists():
# REMOVED_UNUSED_CODE:             if not overwrite:
# REMOVED_UNUSED_CODE:                 logger.warning(f"File `{targetfile}` exists already, not deploying sample file.")
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE:             logger.warning(f"File `{targetfile}` exists already, overwriting.")
# REMOVED_UNUSED_CODE:         shutil.copy(str(sourcedir / source), str(targetfile))
