# Sudoers Configuration Issue

## Problem

The `/etc/sudoers.d/claude` file has incorrect ownership, which completely breaks sudo functionality.

**Current state:**
```
-r--r----- 1 claude claude 29 Jan  9 11:19 /etc/sudoers.d/claude
```

**Required state:**
```
-r--r----- 1 root root 29 Jan  9 11:19 /etc/sudoers.d/claude
```

## Symptoms

When sudo is broken, you'll see errors like:
```
sudo: /etc/sudoers.d/claude is owned by uid 1000, should be 0
sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper
sudo: a password is required
```

## Fix

Run these commands as root (from the Incus host or during image build):

```bash
chown root:root /etc/sudoers.d/claude
chmod 440 /etc/sudoers.d/claude
```

## File Contents

The file content is correct, only the ownership is wrong:
```
claude ALL=(ALL) NOPASSWD:ALL
```

## Prevention

When creating the sudoers file in your image build process, ensure proper ownership:

```bash
echo "claude ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/claude
chown root:root /etc/sudoers.d/claude
chmod 440 /etc/sudoers.d/claude
```

Or use a heredoc with proper permissions:

```bash
cat <<EOF | install -m 440 -o root -g root /dev/stdin /etc/sudoers.d/claude
claude ALL=(ALL) NOPASSWD:ALL
EOF
```
