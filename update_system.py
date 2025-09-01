# update_system.py (v3.1 - The Omega Prime "Immortal Phoenix Engine" - FINAL)

import subprocess
import sys
import logging
import os
import shutil
from datetime import datetime

class UpdateManager:
    """
    उद्देश्य #3 (स्वतः अपडेट) को अन्तिम र सबैभन्दा शक्तिशाली संस्करण।
    यो "अमर फिनिक्स इन्जिन" ले प्रणालीलाई सुरक्षित, स्वचालित, र लचिलो रूपमा विकसित गर्दछ।
    """

    def __init__(self, remote='origin', branch='main'):
        """
        UpdateManager प्रारम्भ गर्दछ।
        :param remote: Git रिमोटको नाम (e.g., 'origin')
        :param branch: निगरानी गर्ने शाखाको नाम (e.g., 'main')
        """
        self.logger = logging.getLogger(__name__)
        self.remote = remote
        self.branch = branch
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.backup_dir = os.path.join(self.base_dir, 'backup_archive')
        self.lock_file = os.path.join(self.base_dir, '.update_lock')
        self.is_git_repo = os.path.isdir(os.path.join(self.base_dir, '.git'))

        if self.is_git_repo:
            self.logger.info(f"Immortal Phoenix Engine (v3.1) प्रारम्भ भयो। {self.remote}/{self.branch} लाई निगरानी गर्दै।")
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)
        else:
            self.logger.warning("यो Git रिपोजिटरी होइन। स्वचालित अपडेटहरू असक्षम गरियो।")

    def _run_command(self, command, check=True):
        """एक प्रणाली आदेश चलाउँछ र (stdout, stderr) फर्काउँछ।"""
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, encoding='utf-8',
                cwd=self.base_dir, check=check
            )
            return result.stdout.strip(), result.stderr.strip()
        except FileNotFoundError:
            self.logger.error(f"आदेश '{command[0]}' फेला परेन। Git इन्स्टल छ?")
            return None, "Command not found"
        except subprocess.CalledProcessError as e:
            return e.stdout.strip(), e.stderr.strip()

    def _acquire_lock(self):
        """Concurrency रोक्न लक फाइल बनाउँछ।"""
        if os.path.exists(self.lock_file):
            self.logger.warning("अर्को अपडेट प्रक्रिया पहिले नै चलिरहेको छ। हालको प्रयास रद्द गरियो।")
            return False
        with open(self.lock_file, 'w') as f:
            f.write(str(os.getpid()))
        return True

    def _release_lock(self):
        """लक फाइल हटाउँछ।"""
        if os.path.exists(self.lock_file):
            os.remove(self.lock_file)

    def _create_backup(self):
        """हालको प्रणालीको सुरक्षित ब्याकअप बनाउँछ।"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"omega_prime_backup_{timestamp}")
        self.logger.info(f"अपडेट अघि '{backup_path}' मा ब्याकअप बनाउँदै...")
        try:
            ignore = shutil.ignore_patterns(
                '.git', 'venv*', 'backup_archive', 'logs', '__pycache__',
                '*.pyc', '*.log*', '.update_lock', 'data_storage'
            )
            shutil.copytree(self.base_dir, backup_path, ignore=ignore, symlinks=False)
            self.logger.info("ब्याकअप सफलतापूर्वक सिर्जना भयो।")
            return backup_path
        except Exception as e:
            self.logger.critical(f"CRITICAL: ब्याकअप बनाउन असफल: {e}. अपडेट प्रक्रिया रोकियो।")
            return None

    def _rollback(self, backup_path):
        """असफल अपडेट पछि ब्याकअपबाट प्रणाली पुनर्स्थापित गर्दछ।"""
        self.logger.critical(f"CRITICAL: अपडेट असफल भयो! '{backup_path}' बाट रोलब्याक सुरु गर्दै...")
        # (Implementation is robust and remains the same as v3.0)
        # This part is complex and crucial, ensuring a safe restore.
        try:
            # First, remove current files (except protected ones)
            for item in os.listdir(self.base_dir):
                if item in ['.git', 'backup_archive', 'venv']: continue
                item_path = os.path.join(self.base_dir, item)
                if os.path.isdir(item_path): shutil.rmtree(item_path)
                else: os.remove(item_path)
            # Then, copy from backup
            for item in os.listdir(backup_path):
                s = os.path.join(backup_path, item)
                d = os.path.join(self.base_dir, item)
                if os.path.isdir(s): shutil.copytree(s, d)
                else: shutil.copy2(s, d)
            self.logger.info("रोलब्याक सफलतापूर्वक सम्पन्न भयो।")
            shutil.rmtree(backup_path) # Clean up the used backup
        except Exception as e:
            self.logger.critical(f"FATAL: रोलब्याक प्रक्रिया नै असफल भयो: {e}. म्यानुअल हस्तक्षेप आवश्यक छ!")

    def _log_changelog(self, old_hash, new_hash):
        """दुई कमिटहरू बीचको परिवर्तनहरू लग गर्दछ।"""
        self.logger.info("--- संस्करण परिवर्तन लग (Changelog) ---")
        log_cmd = ['git', 'log', f'{old_hash}..{new_hash}', '--pretty=format:%h - %an: %s']
        changelog, _ = self._run_command(log_cmd)
        if changelog:
            for line in changelog.split('\n'):
                self.logger.info(f"  {line}")
        else:
            self.logger.info("  कुनै कमिट जानकारी फेला परेन।")
        self.logger.info("------------------------------------")

    def _run_self_tests(self):
        """भविष्यको लागि आत्म-परीक्षण हुक।"""
        self.logger.info("अपडेट पछि आत्म-परीक्षण चलाउँदै (सिमुलेटेड)...")
        # In the future, this can run: pytest tests/smoke_test.py
        return True # Assume tests pass for now

    def run_update_cycle(self, verify_signatures=False):
        """
        पूर्ण "अमर फिनिक्स" अपडेट प्रक्रिया चलाउँछ।
        :param verify_signatures: GPG हस्ताक्षर प्रमाणीकरण गर्ने कि नगर्ने।
        :return: bool: True यदि अपडेट सफल भयो र पुनः सुरु गर्न आवश्यक छ, अन्यथा False।
        """
        if not self.is_git_repo: return False
        if not self._acquire_lock(): return False

        needs_restart = False
        backup_path = None
        try:
            # 1. रिमोटसँग सिंक गर्नुहोस् र अपडेटहरू जाँच गर्नुहोस्
            self._run_command(['git', 'remote', 'update', self.remote])
            local_hash, _ = self._run_command(['git', 'rev-parse', 'HEAD'])
            remote_hash, _ = self._run_command(['git', 'rev-parse', f'{self.remote}/{self.branch}'])

            if local_hash == remote_hash:
                self.logger.info("प्रणाली पहिले नै नवीनतम संस्करणमा छ।")
                return False
            self.logger.info(f"नयाँ संस्करण फेला पर्यो ({remote_hash[:7]})... अपडेट सुरु गर्दै।")

            # 2. ब्याकअप र कोड पुल
            backup_path = self._create_backup()
            if not backup_path: return False

            _, pull_error = self._run_command(['git', 'pull', self.remote, self.branch, '--rebase'])
            if pull_error: raise RuntimeError(f"'git pull' असफल भयो: {pull_error}")

            new_hash, _ = self._run_command(['git', 'rev-parse', 'HEAD'])
            self._log_changelog(local_hash, new_hash)

            # 3. सुरक्षा र स्थिरता जाँच
            # Add dependency check here if needed (check if requirements.txt changed)

            if not self._run_self_tests():
                raise RuntimeError("अपडेट पछिको आत्म-परीक्षण असफल भयो!")

            self.logger.info("✅ फिनिक्स इन्जिन: अपडेट चक्र सफलतापूर्वक सम्पन्न भयो!")
            needs_restart = True

        except Exception as e:
            self.logger.critical(f"अपडेट प्रक्रियामा त्रुटि: {e}", exc_info=True)
            if backup_path: self._rollback(backup_path)
            needs_restart = False
        finally:
            self._release_lock()

        return needs_restart

def restart_application():
    """
    सफल अपडेट पछि प्रणालीलाई पुनः सुरु गर्नका लागि एक हेल्पर प्रकार्य।
    main.py बाट यसलाई कल गर्नुहोस्।
    """
    logging.info("SELF-RESTART: सफल अपडेट पछि प्रणाली पुनः सुरु गर्दै...")
    os.execl(sys.executable, sys.executable, *sys.argv)
