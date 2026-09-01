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

## 5. Understand the Linux and Windows filesystems

Your Ubuntu home directory is represented by:

```bash
~
```

Display it using:

```bash
pwd
```

Windows drives are available under `/mnt`. For example:

```text
C:\Users\Student\Documents
```

is accessible from Ubuntu as:

```text
/mnt/c/Users/Student/Documents
```

For programming and bioinformatics analyses, keep active projects in the Linux home directory, for example:

```bash
mkdir -p ~/courses
cd ~/courses
```

Working inside `~/courses` normally provides better performance and fewer file-permission problems than running analyses directly under `/mnt/c/`.

Windows File Explorer can display the current Ubuntu directory using:

```bash
explorer.exe .
```

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

### 7.6 Prevent automatic activation of the base environment

For this course, it is clearer to activate named environments explicitly. Run:

```bash
conda config --set auto_activate_base false
```

Close and reopen Ubuntu. The `(base)` label should no longer appear automatically.

Conda remains available:

```bash
conda --version
```

## 8. Create the course environment

Create a dedicated environment rather than installing course packages in the base environment:

```bash
conda create -n sbi-courses python=3.12 -y
```

Activate it:

```bash
conda activate sbi-courses
```

The prompt should begin with:

```text
(sbi-courses)
```

Verify the active Python installation:

```bash
which python
python --version
```

The path printed by `which python` should contain:

```text
anaconda3/envs/sbi-courses
```

Deactivate the environment when finished:

```bash
conda deactivate
```

## 9. Test the installation

Open Ubuntu and run:

```bash
conda activate sbi-courses
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

## 10. Starting Ubuntu in future sessions

Students can start Ubuntu in any of these ways:

- Open **Ubuntu 24.04 LTS** from the Start menu.
- Open Windows Terminal and select the Ubuntu profile.
- Open PowerShell and run `wsl`.

At the beginning of a practical session, activate the course environment:

```bash
conda activate sbi-courses
```

## 11. Common problems

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

### The Linux password appears not to work

No characters are displayed while entering a password in Ubuntu. Type it carefully and press **Enter**.

### Insufficient disk space

Anaconda and future bioinformatics environments require several gigabytes of storage. Remove unnecessary files or use Miniconda after consulting the course instructor.

## 12. Installation checklist

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
conda activate sbi-courses
python --version
which python
```

The setup is complete when:

- Ubuntu is version 24.04 LTS;
- Ubuntu runs under WSL version 2;
- Git is available;
- conda is available inside Ubuntu;
- the `sbi-courses` environment activates successfully; and
- Python runs from the `sbi-courses` environment.

## Official references

- [Install WSL — Microsoft](https://learn.microsoft.com/windows/wsl/install)
- [Basic WSL commands — Microsoft](https://learn.microsoft.com/windows/wsl/basic-commands)
- [Install Anaconda on Linux — Anaconda](https://www.anaconda.com/docs/getting-started/anaconda/install/linux-install)
- [Anaconda installer archive](https://repo.anaconda.com/archive/)

