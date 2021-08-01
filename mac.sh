pip install -r flask_app/requirements.txt
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install redis
brew services start redis
python3 -m flask_app.app