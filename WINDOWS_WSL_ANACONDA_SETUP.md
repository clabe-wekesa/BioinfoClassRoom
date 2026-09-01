# Windows Setup for SBI 811 and SBI 812

This guide prepares a Windows computer for the practical sessions in:

- **SBI 811: Computer Programming in Bioinformatics**
- **SBI 812: Machine Learning in Bioinformatics**

Students will install:

1. Windows Subsystem for Linux 2 (WSL 2)
2. Ubuntu 24.04 LTS
3. Anaconda Distribution inside Ubuntu

> **Important:** Install Anaconda inside Ubuntu, not as a separate Windows installation. This ensures that Bash, Python, conda and later bioinformatics tools operate in the same Linux environment.

## 1. Check the Windows version

These instructions require either:

- Windows 11; or
- Windows 10 version 2004 or later, build 19041 or later.

To check the installed version:

1. Press **Windows key + R**.
2. Enter `winver`.
3. Select **OK**.

Install pending Windows updates before continuing.

## 2. Enable WSL and install Ubuntu 24.04 LTS

### 2.1 Open PowerShell as an administrator

1. Open the **Start** menu.
2. Search for **PowerShell**.
3. Right-click **Windows PowerShell** or **Terminal**.
4. Select **Run as administrator**.
5. Approve the security prompt.

The window should show PowerShell, usually with a prompt similar to:

```powershell
PS C:\Windows\System32>
```

### 2.2 Update WSL

Run:

```powershell
wsl --update
```

Set WSL 2 as the default for new Linux installations:

```powershell
wsl --set-default-version 2
```

### 2.3 Confirm the Ubuntu 24.04 distribution name

Run:

```powershell
wsl --list --online
```

Find Ubuntu 24.04 LTS in the displayed list. Its distribution name should normally be `Ubuntu-24.04`.

### 2.4 Install Ubuntu 24.04 LTS

Run:

```powershell
wsl --install -d Ubuntu-24.04
```

If the installation remains at `0.0%`, try:

```powershell
wsl --install --web-download -d Ubuntu-24.04
```

Restart the computer if Windows asks you to do so.

### 2.5 First Ubuntu launch

After restarting:

1. Open the **Start** menu.
2. Search for **Ubuntu 24.04 LTS**.
3. Open it.
4. Wait while Ubuntu completes its initial setup.
5. Create a Linux username when prompted.
6. Create a Linux password.

The Linux username does not need to be identical to the Windows username.

> **Password note:** Ubuntu does not display dots, stars or other characters while a password is being typed. This is normal. Type the password and press **Enter**.

Do not forget this password. It will be required when using `sudo`.

## 3. Verify that Ubuntu uses WSL 2

Close Ubuntu and open PowerShell. Run:

```powershell
wsl --list --verbose
```

The result should resemble:

```text
  NAME            STATE           VERSION
* Ubuntu-24.04    Stopped         2
```

The `VERSION` column must show `2`.

If it shows `1`, run:

```powershell
wsl --set-version Ubuntu-24.04 2
```

## 4. Update Ubuntu

Open **Ubuntu 24.04 LTS** from the Start menu.

From this point onward, commands are Ubuntu/Linux commands. Do not run them in PowerShell.

Update the package lists and installed software:

```bash
sudo apt update
sudo apt upgrade -y
```

Enter the Linux password when requested.

Install utilities needed during setup:

```bash
sudo apt install -y curl wget git build-essential
```

Verify Ubuntu:

```bash
lsb_release -a
```

The output should identify Ubuntu 24.04 LTS.

Verify Git:

```bash
git --version
```

## 5. Open Ubuntu directly in any course folder

Windows drives are available under `/mnt`. For example:

```text
C:\Users\Student\Documents
```

is accessible from Ubuntu as:

```text
/mnt/c/Users/Student/Documents
```

For the introductory practicals, students can create an easily accessible Windows folder such as:

```text
C:\SBI-courses
```

### 5.1 Set Ubuntu as the default Windows Terminal profile

This setup is required only once:

1. Open **Windows Terminal**.
2. Select the arrow beside the **+** button.
3. Select **Settings**.
4. Under **Startup**, set **Default profile** to **Ubuntu-24.04**.
5. Select **Save**.

Windows Terminal automatically creates an Ubuntu profile after WSL Ubuntu is installed.

### 5.2 Open Linux in a selected folder

1. Open File Explorer.
2. Navigate to the desired folder, for example `C:\SBI-courses`.
3. Right-click an empty area inside the folder. On some Windows versions, hold **Shift** while right-clicking.
4. Select **Open in Terminal** or **Open Linux shell here**, depending on the Windows version.

Because Ubuntu is the default terminal profile, the terminal should open as an Ubuntu shell in that folder.

If **Open in Terminal** opens PowerShell instead, enter:

```powershell
wsl
```

WSL will enter Linux while retaining the same working folder.

Verify the location using:

```bash
pwd
```

For `C:\SBI-courses`, Ubuntu should show:

```text
/mnt/c/SBI-courses
```

### 5.3 Alternative method using the File Explorer address bar

Navigate to a folder in File Explorer, click the address bar, enter:

```text
wsl
```

and press **Enter**. This opens an Ubuntu shell in the selected folder.

### 5.4 Access Linux files from Windows

Ubuntu's Linux home directory is represented by:

```bash
~
```

Windows File Explorer can display the current Ubuntu directory using:

```bash
explorer.exe .
```

For early Bash and Python exercises, working in `C:\SBI-courses` is convenient. For large RNA-seq files and compute-intensive BOTAS analyses, the instructor may later ask students to work under `~/courses`, because Linux tools normally perform better in the WSL filesystem than under `/mnt/c/`.

## 6. Check the computer architecture

In Ubuntu, run:

```bash
uname -m
```

Most Windows computers will report:

```text
x86_64
```

The Anaconda command in the next section is for `x86_64`. If the result is `aarch64`, use the ARM64 installer from the official Anaconda Linux installation page instead.

## 7. Install Anaconda inside Ubuntu

The commands below install Anaconda Distribution 2026.07-1 for 64-bit x86 Linux. The course may update the pinned installer version in future years.

### 7.1 Move to the home directory

```bash
cd ~
```

### 7.2 Download the Anaconda installer

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2026.07-1-Linux-x86_64.sh
```

### 7.3 Optional but recommended: verify the installer

Generate its SHA-256 checksum:

```bash
sha256sum Anaconda3-2026.07-1-Linux-x86_64.sh
```

Compare the result with the checksum published for the same filename at:

https://repo.anaconda.com/archive/

Do not continue if the checksum is different.

### 7.4 Run the installer

```bash
bash Anaconda3-2026.07-1-Linux-x86_64.sh
```

During installation:

1. Press **Enter** to begin.
2. Read or scroll through the licence using **Enter** or the space bar.
3. Enter `yes` to accept the terms.
4. Press **Enter** to accept the default installation path, normally `/home/YOUR_USERNAME/anaconda3`.
5. Enter `yes` when asked whether the installer should initialize Anaconda.

Do not install Anaconda using `sudo` and do not install it under `/root`.

### 7.5 Activate conda

Refresh the terminal configuration:

```bash
source ~/.bashrc
```

The prompt may now begin with `(base)`.

Verify the installation:

```bash
conda --version
python --version
conda list
```

### 7.6 Keep the base environment active

The installer initializes conda so that its base environment activates whenever Ubuntu starts. The command prompt should begin with:

```text
(base)
```

For these courses, students will use this shared base environment unless the instructor gives different instructions. Packages installed during the course will therefore be available in later practical sessions.

Verify the active Python installation:

```bash
which python
python --version
```

The path printed by `which python` should normally contain:

```text
anaconda3/bin/python
```

Install packages without `sudo`, for example:

```bash
conda install PACKAGE_NAME
```

Do not use `sudo pip install` or `sudo conda install`. Those commands can mix system-level and Anaconda-managed packages and create permission problems.

## 8. Test the installation

Open Linux in the course folder using **Open in Terminal** or **Open Linux shell here**, confirm that `(base)` appears, and run:

```bash
python
```

At the Python prompt, enter:

```python
sequence = "ATGCGCTA"
gc = (sequence.count("G") + sequence.count("C")) / len(sequence) * 100
print(gc)
```

The result should be:

```text
50.0
```

Exit Python:

```python
exit()
```

## 9. Starting a practical session in the required folder

1. Open the course folder in File Explorer.
2. Right-click an empty area, using **Shift + right-click** where necessary.
3. Select **Open in Terminal** or **Open Linux shell here**.
4. Confirm that the prompt begins with `(base)`.
5. Run `pwd` to confirm that the terminal opened in the correct folder.

There is no need to open Ubuntu from the Start menu or manually activate the base environment.

## 10. Common problems

### `wsl` is not recognized

Install all Windows updates, restart the computer and try the installation again from an administrator PowerShell window.

### WSL installation displays help instead of installing

List available distributions:

```powershell
wsl --list --online
```

Then install the exact displayed name for Ubuntu 24.04.

### Virtualization error

WSL 2 requires hardware virtualization. Enable virtualization in the computer's BIOS/UEFI settings. Depending on the processor and manufacturer, it may be called **Intel Virtualization Technology**, **Intel VT-x**, **AMD-V** or **SVM Mode**.

### `conda: command not found`

Run:

```bash
~/anaconda3/bin/conda init bash
source ~/.bashrc
```

Then check:

```bash
conda --version
```

### `(base)` does not appear automatically

Run:

```bash
~/anaconda3/bin/conda init bash
source ~/.bashrc
```

Close the terminal and open it again in the course folder.

### **Open in Terminal** starts PowerShell

Either enter `wsl` to switch to Ubuntu in the same folder, or set **Ubuntu-24.04** as the default profile under **Windows Terminal → Settings → Startup**.

### The Linux password appears not to work

No characters are displayed while entering a password in Ubuntu. Type it carefully and press **Enter**.

### Insufficient disk space

Anaconda and future bioinformatics environments require several gigabytes of storage. Remove unnecessary files or use Miniconda after consulting the course instructor.

## 11. Installation checklist

Run the following commands and confirm that none produces an error:

In PowerShell:

```powershell
wsl --list --verbose
```

In Ubuntu:

```bash
lsb_release -a
git --version
conda --version
python --version
which python
```

The setup is complete when:

- Ubuntu is version 24.04 LTS;
- Ubuntu runs under WSL version 2;
- Git is available;
- conda is available inside Ubuntu;
- the `(base)` environment activates automatically;
- Python runs from the Anaconda base environment; and
- Ubuntu can be opened directly inside a selected course folder.

## Official references

- [Install WSL — Microsoft](https://learn.microsoft.com/windows/wsl/install)
- [Basic WSL commands — Microsoft](https://learn.microsoft.com/windows/wsl/basic-commands)
- [Install Anaconda on Linux — Anaconda](https://www.anaconda.com/docs/getting-started/anaconda/install/linux-install)
- [Anaconda installer archive](https://repo.anaconda.com/archive/)
