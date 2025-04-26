# WSL (The Windows Subsystem for Linux)

## Resources

https://learn.microsoft.com/en-us/windows/wsl/install
https://learn.microsoft.com/en-us/windows/wsl/setup/environment

## Prerequisites

Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11

## Installation

```bash
wsl --install
```

## Check WSL versions

```bash
wsl --list --verbose #Long version
wsl -l -v            #Short version
```

if `wsl -v` doesn't work - you have WSL 1 version

## Check distribution online (to install)

```bash
wsl --list --online  #Long version
wsl -l -o            #Short version
```

## Check distribution locally (installed)

```bash
wsl --list  #Long version
wsl -l      #Short version
```

## Install distribution

```bash
wsl --list --online  #Check avaiable distribution
wsl --install [distro_name] [options] #Options in wsl --help
```

## Change version of WSL for distro

```bash
wsl --set-version [distro_name] 2 #will use WSL 2 for distro
wsl --set-version [distro_name] 1 #will use WSL 1 for distro
```

## Change defualt version of WSL for distro

```bash
wsl --set-default-version [version] #Will use WSL 1/2 by default for installing distro
```

## Shutdown WSL2 and all distributions

```bash
wsl --shut-down
```

## Run distro with root permission

It can be usefull to change user password inside Linux by `passwd [user]`

```bash
wsl -d [distribution] -u root
```