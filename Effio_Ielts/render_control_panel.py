#!/usr/bin/env python3
"""
Render Control Panel - Monitor and manage your Django app deployment
Usage: python render_control_panel.py
"""

import requests
import time
import json
from datetime import datetime
import subprocess
import sys
import webbrowser
from pathlib import Path

# Configuration
APP_URL = "https://quizapp-rx2d.onrender.com"
GITHUB_REPO = "tamTrantam/QuizApp"
LOCAL_PROJECT_PATH = Path(__file__).parent

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class RenderControlPanel:
    def __init__(self):
        self.app_url = APP_URL

    def print_header(self):
        """Print the control panel header"""
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.WHITE}🚀 RENDER CONTROL PANEL 🚀{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BLUE}App URL: {Colors.WHITE}{self.app_url}{Colors.END}")
        print(f"{Colors.BLUE}Time: {Colors.WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

    def check_health(self):
        """Check if the app is responding"""
        try:
            response = requests.get(f"{self.app_url}/", timeout=10)
            if response.status_code == 200:
                return f"{Colors.GREEN}✅ ONLINE{Colors.END}", response.status_code, response.elapsed.total_seconds()
            else:
                return f"{Colors.YELLOW}⚠️  ISSUES{Colors.END}", response.status_code, response.elapsed.total_seconds()
        except requests.exceptions.RequestException as e:
            return f"{Colors.RED}❌ OFFLINE{Colors.END}", "Error", str(e)

    def check_admin_panel(self):
        """Check admin panel accessibility"""
        try:
            response = requests.get(f"{self.app_url}/admin/", timeout=10)
            if response.status_code == 200:
                return f"{Colors.GREEN}✅ ACCESSIBLE{Colors.END}", response.status_code
            elif response.status_code == 302:  # Redirect to login
                return f"{Colors.GREEN}✅ REDIRECT TO LOGIN{Colors.END}", response.status_code
            else:
                return f"{Colors.YELLOW}⚠️  ISSUES{Colors.END}", response.status_code
        except requests.exceptions.RequestException as e:
            return f"{Colors.RED}❌ ERROR{Colors.END}", str(e)

    def check_static_files(self):
        """Check if static files are being served"""
        static_urls = [
            f"{self.app_url}/static/css/main.css",
            f"{self.app_url}/static/admin/css/base.css"
        ]
        
        results = []
        for url in static_urls:
            try:
                response = requests.head(url, timeout=5)
                if response.status_code == 200:
                    results.append(f"{Colors.GREEN}✅{Colors.END}")
                else:
                    results.append(f"{Colors.RED}❌{Colors.END}")
            except:
                results.append(f"{Colors.RED}❌{Colors.END}")
        
        return results

    def test_authentication(self):
        """Test authentication endpoints"""
        auth_endpoints = [
            "/accounts/login/",
            "/accounts/signup/",
            "/accounts/logout/"
        ]
        
        results = {}
        for endpoint in auth_endpoints:
            try:
                response = requests.get(f"{self.app_url}{endpoint}", timeout=5)
                if response.status_code in [200, 302]:
                    results[endpoint] = f"{Colors.GREEN}✅{Colors.END}"
                else:
                    results[endpoint] = f"{Colors.RED}❌ ({response.status_code}){Colors.END}"
            except:
                results[endpoint] = f"{Colors.RED}❌ ERROR{Colors.END}"
        
        return results

    def get_git_status(self):
        """Get local git status"""
        try:
            # Check if there are uncommitted changes
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=LOCAL_PROJECT_PATH)
            uncommitted_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            uncommitted = len(uncommitted_files)
            
            # Get latest commit
            result = subprocess.run(['git', 'log', '-1', '--oneline'], 
                                  capture_output=True, text=True, cwd=LOCAL_PROJECT_PATH)
            latest_commit = result.stdout.strip()
            
            # Check current branch
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True, cwd=LOCAL_PROJECT_PATH)
            current_branch = result.stdout.strip()
            
            return {
                'branch': current_branch,
                'latest_commit': latest_commit,
                'uncommitted_changes': uncommitted
            }
        except:
            return {'error': 'Git not available'}

    def deploy_latest(self):
        """Deploy latest changes to Render"""
        print(f"\n{Colors.YELLOW}🚀 Deploying latest changes...{Colors.END}")
        
        try:
            # Add all changes
            subprocess.run(['git', 'add', '.'], cwd=LOCAL_PROJECT_PATH, check=True)
            
            # Commit with timestamp
            commit_msg = f"Deploy update - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_msg], cwd=LOCAL_PROJECT_PATH, check=True)
            
            # Push to trigger deployment
            subprocess.run(['git', 'push', 'origin', 'main'], cwd=LOCAL_PROJECT_PATH, check=True)
            
            print(f"{Colors.GREEN}✅ Successfully pushed to GitHub! Render will auto-deploy.{Colors.END}")
            print(f"{Colors.BLUE}💡 Check deployment status in 2-3 minutes.{Colors.END}")
            
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}❌ Error during deployment: {e}{Colors.END}")

    def run_health_monitor(self, duration=60):
        """Monitor app health for specified duration"""
        print(f"\n{Colors.PURPLE}🔍 Monitoring app health for {duration} seconds...{Colors.END}")
        print(f"{Colors.BLUE}Press Ctrl+C to stop{Colors.END}\n")
        
        start_time = time.time()
        check_count = 0
        success_count = 0
        
        try:
            while time.time() - start_time < duration:
                status, code, response_time = self.check_health()
                check_count += 1
                
                if "ONLINE" in status:
                    success_count += 1
                
                timestamp = datetime.now().strftime('%H:%M:%S')
                if isinstance(response_time, float):
                    print(f"[{timestamp}] Status: {status} | Code: {code} | Response: {response_time:.2f}s")
                else:
                    print(f"[{timestamp}] Status: {status} | Code: {code} | Error: {response_time}")
                
                time.sleep(5)  # Check every 5 seconds
                
        except KeyboardInterrupt:
            pass
        
        uptime_percentage = (success_count / check_count) * 100 if check_count > 0 else 0
        print(f"\n{Colors.CYAN}📊 Monitoring Summary:{Colors.END}")
        print(f"Total checks: {check_count}")
        print(f"Successful: {success_count}")
        print(f"Uptime: {uptime_percentage:.1f}%")

    def show_status_dashboard(self):
        """Display comprehensive status dashboard"""
        self.print_header()
        
        # App Health
        print(f"{Colors.BOLD}🌐 App Health:{Colors.END}")
        status, code, response_time = self.check_health()
        print(f"   Status: {status}")
        print(f"   HTTP Code: {code}")
        if isinstance(response_time, float):
            print(f"   Response Time: {response_time:.2f}s")
        print()
        
        # Admin Panel
        print(f"{Colors.BOLD}⚙️  Admin Panel:{Colors.END}")
        admin_status, admin_code = self.check_admin_panel()
        print(f"   Status: {admin_status}")
        print(f"   HTTP Code: {admin_code}")
        print()
        
        # Static Files
        print(f"{Colors.BOLD}📁 Static Files:{Colors.END}")
        static_results = self.check_static_files()
        print(f"   Main CSS: {static_results[0]}")
        print(f"   Admin CSS: {static_results[1]}")
        print()
        
        # Authentication
        print(f"{Colors.BOLD}🔐 Authentication:{Colors.END}")
        auth_results = self.test_authentication()
        for endpoint, status in auth_results.items():
            print(f"   {endpoint}: {status}")
        print()
        
        # Git Status
        print(f"{Colors.BOLD}📝 Git Status:{Colors.END}")
        git_status = self.get_git_status()
        if 'error' not in git_status:
            print(f"   Branch: {Colors.CYAN}{git_status['branch']}{Colors.END}")
            print(f"   Latest: {git_status['latest_commit']}")
            if git_status['uncommitted_changes'] > 0:
                print(f"   Uncommitted: {Colors.YELLOW}{git_status['uncommitted_changes']} files{Colors.END}")
            else:
                print(f"   Uncommitted: {Colors.GREEN}None{Colors.END}")
        else:
            print(f"   {Colors.RED}Git not available{Colors.END}")
        print()

    def show_menu(self):
        """Display interactive menu"""
        while True:
            print(f"\n{Colors.BOLD}🎛️  Control Panel Menu:{Colors.END}")
            print(f"{Colors.WHITE}1.{Colors.END} Show Status Dashboard")
            print(f"{Colors.WHITE}2.{Colors.END} Monitor Health (60s)")
            print(f"{Colors.WHITE}3.{Colors.END} Deploy Latest Changes")
            print(f"{Colors.WHITE}4.{Colors.END} Open App in Browser")
            print(f"{Colors.WHITE}5.{Colors.END} Open Admin Panel")
            print(f"{Colors.WHITE}6.{Colors.END} Quick Status Check")
            print(f"{Colors.WHITE}7.{Colors.END} Exit")
            
            choice = input(f"\n{Colors.CYAN}Select option (1-7): {Colors.END}").strip()
            
            if choice == '1':
                self.show_status_dashboard()
            elif choice == '2':
                self.run_health_monitor()
            elif choice == '3':
                self.deploy_latest()
            elif choice == '4':
                webbrowser.open(self.app_url)
                print(f"{Colors.GREEN}🌐 Opened app in browser{Colors.END}")
            elif choice == '5':
                webbrowser.open(f"{self.app_url}/admin/")
                print(f"{Colors.GREEN}⚙️  Opened admin panel in browser{Colors.END}")
            elif choice == '6':
                status, code, response_time = self.check_health()
                print(f"Quick Check: {status} (Code: {code})")
            elif choice == '7':
                print(f"{Colors.GREEN}👋 Goodbye!{Colors.END}")
                break
            else:
                print(f"{Colors.RED}❌ Invalid option. Please try again.{Colors.END}")

def main():
    """Main function"""
    control_panel = RenderControlPanel()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == 'status':
            control_panel.show_status_dashboard()
        elif command == 'monitor':
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            control_panel.run_health_monitor(duration)
        elif command == 'deploy':
            control_panel.deploy_latest()
        elif command == 'quick':
            status, code, response_time = control_panel.check_health()
            print(f"Status: {status} (Code: {code})")
        else:
            print("Usage: python render_control_panel.py [status|monitor|deploy|quick]")
    else:
        control_panel.show_menu()

if __name__ == "__main__":
    main()