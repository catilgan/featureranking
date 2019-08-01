import sys
from fearank.ui.AppContext import AppContext

if __name__ == '__main__':
    app_context = AppContext()
    exit_code = app_context.run()
    input()
    sys.exit(exit_code)
