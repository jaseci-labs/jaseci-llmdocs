# environment


## From: contrib.md

To get setup run
```bash
# Install black
python3 -m venv ~/.jacenv/
source ~/.jacenv/bin/activate
pip3 install pre-commit pytest pytest-xdist
pre-commit install
```

To understand our linting and mypy type checking have a look at our pre-commit actions. You can set up your enviornment accordingly. For help interpreting this if you need it, call upon our friend Mr. ChatGPT or one of his colleagues.


## From: getting_started.md

Firstly make sure that Python 3.12 or higher is installed in your environment, then simply install Jac using pip:

```bash
python -m pip install -U jaclang
```

Once you've got Jaclang installed, just give the Jac CLI a try to make sure everything's up and running smoothly.

- Start the Jac CLI:
    ```bash
    jac --version
    ```
- Run a .jac file
    ```bash
    jac run <file_name>.jac
    ```
- To test run a 'Hello World' Program
    ```bash
    echo "with entry { print('Hello world'); }" > test.jac;
    jac run test.jac;
    rm test.jac;
    ```
> **Note**
>
> If these commands prints ```Hello world``` you are good to go.

## Installing the VS Code Extension

In addition to setting up JacLang itself, you may also want to take advantage of the JacLang language extension for Visual Studio Code (VSCode) or Cursor. This will give you enhanced code highlighting, autocomplete, and other useful language features within your editor environment.

**For VS Code users:**
- Visit the VS Code marketplace and install the [Jac Extension](https://marketplace.visualstudio.com/items?itemName=jaseci-labs.jaclang-extension)

**For Cursor users:**
1. Go to the [latest Jaseci release page](https://github.com/Jaseci-Labs/jaseci/releases/latest)
2. Download the latest `jaclang-extension-*.vsix` file from the release assets
3. Open Cursor
4. Press `Ctrl+ShiftP` (or `Cmd+ShiftP` on Mac)
5. Type `>install from vsix` and select the command
6. Select the downloaded VSIX file
7. The extension will be installed and ready to use


## From: sso_implementation.md

## Steps to implement SSO in Jac cloud Setting Your Environment variables

### Step 1: Obtain relevant client credentials from supported platforms
First choose the supported platform and register your application with the relevant platform to get credentials needed
to setup SSO in jac cloud.You can read following documentations and tutorials to register your application.

### Step 2: Setup relevant env variables
### Basic Pattern

```bash
# Replace PLATFORM with: GOOGLE, GITHUB, FACEBOOK, etc.
export SSO_{PLATFORM}_CLIENT_ID="your_client_id"
export SSO_{PLATFORM}_CLIENT_SECRET="your_client_secret"
```

#### Google Web Example

```bash
export SSO_GOOGLE_CLIENT_ID="123456789-abcdef.apps.googleusercontent.com"
export SSO_GOOGLE_CLIENT_SECRET="GOCSPX-abcdefghijklmnop"
```

#### Google iOS Example

```bash
export SSO_GOOGLE_IOS_CLIENT_ID="123456789-abcdef.apps.googleusercontent.com"
export SSO_GOOGLE_IOS_CLIENT_SECRET="GOCSPX-abcdefghijklmnop"
```

#### Google Android Example

```bash
export SSO_GOOGLE_ANDROID_CLIENT_ID="123456789-abcdef.apps.googleusercontent.com"
export SSO_GOOGLE_ANDROID_CLIENT_SECRET="GOCSPX-abcdefghijklmnop"
```

#### Apple-Specific SSO Configuration

Apple requires a special configuration for client secret generation:

| **Variable** | **Description** |
|--------------|-----------------|
| `SSO_APPLE_CLIENT_ID` | Apple client ID |
| `SSO_APPLE_CLIENT_TEAM_ID` | Apple developer team ID |
| `SSO_APPLE_CLIENT_KEY` | Apple client key |
| `SSO_APPLE_CLIENT_CERTIFICATE_PATH` | Path to Apple client certificate |
| `SSO_APPLE_CLIENT_CERTIFICATE` | Raw Apple client certificate content |

### Step 3: Call Register Callback Endpoint Provided by JAC Cloud

#### 1. Start the Backend Server

Once all the relevant platform specific environment variables are set, run the backend using:

```bash
jac serve main.jac
```

This command will provide the `backendURL` of the FastAPI server.

