import winreg, pathlib, zipfile, tempfile, datetime, random, os

class Settings:
	r_alphabet = '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

class Logger:
	def info(text : str):
		dt = datetime.datetime.now().strftime("%B %d, %Y | %H:%M:%S")
		print(f'{dt} | \033[94mINFO\033[0m | {text}')
	def error(text : str):
		dt = datetime.datetime.now().strftime("\033[90m%B %d, %Y\033[0m | \033[90m%H:%M:%S\033[0m")
		print(f'{dt} | \033[91mERROR\033[0m | {text}')
	def warn(text : str):
		dt = datetime.datetime.now().strftime("%B %d, %Y | %H:%M:%S")
		print(f'{dt} | \033[93mWARNING\033[0m | {text}')

def random_name(alphabet : str, lenght : int) -> str:
	return ''.join(random.choice(alphabet) for _ in range(lenght))

def parse_json(path : str) -> dict:
	with open(path, "r") as file:
		return json.load(file)

def get_telegram_path() -> object:
	try:
		registry = winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT)
		key = winreg.OpenKey(registry, "tdesktop.tg\\shell\\open\\command")

		path = winreg.EnumValue(key, 0)[1]
		return pathlib.Path(path[1:-10]).parent
	except:
		return None

def is_tdata_in_folder(path : pathlib.Path) -> bool:
	if ((path / 'tdata').is_dir()):
		return True
	return False

def kill_telegram_process():
    for proc in psutil.process_iter():
        if proc.name() == 'Telegram.exe':
            if(check_process_exist_by_name(name)):
                Logger.info('Successfully killed Telegram process.')
            else:
                Logger.warn('Unsuccessfully killed Telegram process.')
            return

def kill_telegram_process_windows():
    os.system("taskkill /f /im Telegram.exe > nul")
    Logger.info('Killed Telegram process.')

def save_tdata_in_archive(zip_file, path : pathlib.Path):
	for file in path.iterdir():
		if file.is_file():
			zip_file.write(file.resolve())
		elif file.is_dir() and not file.name.startswith('user_data'):
			save_tdata_in_archive(zip_file, file.resolve())

def get_telegram_logs(path : pathlib.Path):
	logs = []

	for file in path.iterdir():
		if file.is_file() and file.name.startswith('log'):
			logs.append(file)

	return logs


def main():
	telegram_path = get_telegram_path()
	temp_dir = tempfile.gettempdir()

	tdata_export_name = f'{temp_dir}\\{random_name(Settings.r_alphabet, 25)}_tdata.zip'
	logs_export_name = f'{temp_dir}\\{random_name(Settings.r_alphabet, 25)}_logs.zip'

	if (telegram_path == None):
		Logger.error("Telegram Path not found.")
		exit(1)

	if (is_tdata_in_folder(telegram_path)):
		kill_telegram_process_windows()
		with zipfile.ZipFile(tdata_export_name, 'w') as zip_file:
			save_tdata_in_archive(zip_file, telegram_path / 'tdata')
		Logger.info(f"Successfully saved TData. ({tdata_export_name})")
	else:
		Logger.warn("TData not found in Default location.")

	telegram_logs = get_telegram_logs(telegram_path)

	if len(telegram_logs) > 0:
		with zipfile.ZipFile(logs_export_name, 'w') as zip_file:
			for log in telegram_logs:
				zip_file.write(log, log.name)
			Logger.info(f"Successfully saved Telegram Logs. ({logs_export_name})")
	else:
		Logger.warn(f"Telegram Logs not found.")

if __name__ == '__main__':
	main()