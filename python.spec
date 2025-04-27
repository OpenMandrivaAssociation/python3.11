# Not really -- but python's build system enables lto in its own
# different way, no need for 2 conflicting approaches
%define _disable_lto 1

# Barfs on supposed-to-fail parts of the testsuite
%define _python_bytecompile_build 0

# Python modules aren't linked to libpython%{dirver}
%define _disable_ld_no_undefined 1

%define docver %{version}
%define dirver %(echo %{version} |cut -d. -f1-2)
%define familyver 3

%define api %{dirver}
%define major 1
%define libname %mklibname python %{api} %{major}
%define devname %mklibname python -d
%define staticname %mklibname python -d -s
%define lib32name %mklib32name python %{api} %{major}
%define dev32name %mklib32name python -d

%if %{cross_compiling}
# Because we currently miss libclang_rt.profile-riscv64.a
# in crosscompilers, and python's build system builds
# profiling code
%define prefer_gcc 1
%endif

#define pre rc2

%ifarch %{ix86} %{x86_64} ppc
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

# Let's make tkinter optional -- we may not have more obscure
# stuff like TCL/Tk when bootstrapping a new architecture
%bcond_without tkinter

# weird stuff
# pip not available if python package built with pip
# * build without pip files lead to good package
# * but next package lead to unpackaged pip files 
# let's disable pip
%bcond_with pip

Summary:	An interpreted, interactive object-oriented programming language
Name:		python
# WARNING
# When updating to a new major version (e.g. 3.11 to 3.12, not 3.11.1
# to 3.11.2), make sure you don't break dnf.
# For dnf and abf-console-client to work, you have to rebuild the following packages against
# the new version of python:
#	[disable rpmlint for now -- it needs python-rpm. Set _nonzero_exit_pkgcheck_terminate_build to 0 in ~/.rpmmacros]
#	python-setuptools (may need to be rebuilt twice to catch dependencies)
#	file [for python-magic]
#	rpm [for python-rpm]
#	libdnf
#	libcomps
#	gpgme
#	rpmlint
#	[at this point you can re-enable rpmlint in ~/.rpmmacros]
#	python-packaging
#	python-parsing
#	python-docutils
#	python-alabaster
#	python-pytz
#	python-babel
#	python-markupsafe
#	python-jinja2
#	python-pygments
#	python-charset-normalizer
#	python-idna
#	python-imagesize
#	python-urllib3
#	python-certifi
#	python-requests
#	python-snowballstemmer
#	python-sphinxcontrib-applehelp
#	python-sphinxcontrib-devhelp
#	python-sphinxcontrib-htmlhelp
#	python-sphinxcontrib-jsmath
#	python-sphinxcontrib-qthelp
#	python-sphinxcontrib-serializinghtml
#	python-sphinxcontrib-websupport
#	python-sphinx
#	python-bugzilla
#	dnf
#	python-six
#	python-pip
#	python-dateutil
#	dbus-python
#	dnf-plugins-core
#	python-beaker
#	python-yaml
#	abf-console-client
#	python-templated-dictionary
#	mock
# After getting all related packages into abf, run a mass build to
# adapt the other packages.
# (See the pyup script in the python package source directory
# for an example of how to update)
Version:	3.13.3
Release:	%{?pre:0.%{pre}.}1
License:	Modified CNRI Open Source License
Group:		Development/Python
Url:		https://www.python.org/
Source0:	http://www.python.org/ftp/python/%{version}/Python-%{version}%{?pre:%{pre}}.tar.xz
Source1:	http://www.python.org/ftp/python/doc/%{docver}/python-%{docver}-docs-html.tar.bz2
Source2:	python3.macros
Source3:	pybytecompile.macros
Source4:	macros.buildsys.python
Source100:	%{name}.rpmlintrc

BuildRequires:	autoconf
BuildRequires:	autoconf-archive
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	db-devel
BuildRequires:	gdbm-devel
BuildRequires:	gmp-devel
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libffi) >= 3.1
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(uuid)
#BuildRequires:	python2
%if %{with valgrind}
BuildRequires:	valgrind-devel
%endif
BuildConflicts:	python-pyxml
%ifnarch %{riscv}
BuildRequires:	clang
BuildRequires:	llvm-bolt
%endif
Requires:	%{libname} = %{EVRD}
Obsoletes:	python3 < %{EVRD}
Provides:	python3 = %{EVRD}
Provides:	python(abi) = %{dirver}
Provides:	%{_bindir}/python%{dirver}mu
Provides:	%{_bindir}/python3
Provides:	%{_bindir}/python
%if %{with tkinter}
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
Conflicts:	tkinter3 < %{EVRD}
%endif
Conflicts:	%{libname}-devel < 3.1.2-4
Conflicts:	%{devname} < 3.2.2-3
Conflicts:	python-pyxml

# Used to be separate packages, bundled with core now
%rename	python-ctypes
%rename	python-elementtree
%rename	python-base
%if %{with pip}
%rename	python-setuptools
%rename	python-pkg-resources
Provides:	python3egg(setuptools)
Provides:	python3egg(distribute)
%endif

%patchlist
https://src.fedoraproject.org/rpms/python3.13/raw/rawhide/f/00251-change-user-install-location.patch
https://src.fedoraproject.org/rpms/python3.11/raw/rawhide/f/00328-pyc-timestamp-invalidation-mode.patch
https://src.fedoraproject.org/rpms/python3.13/raw/rawhide/f/00454-invoke-regen-token-rst-with-rstfile-as-an-argument.patch
https://src.fedoraproject.org/rpms/python3.13/raw/rawhide/f/00456-find-the-correct-group-name-in-test_group_no_follow_symlinks.patch
https://src.fedoraproject.org/rpms/python3.13/raw/rawhide/f/00459-apply-intel-control-flow-technology-for-x86-64.patch

python-3.6.2-clang-5.0.patch
Python-3.8.0-c++.patch
# FIXME check if this is still needed (the code has changed a lot
# and claims to support C++ now)
#python-3.8.0-c++atomics.patch
python-3.7.1-dont-build-testembed-with-c++.patch
00201-fix-memory-leak-in-gdbm.patch
python-3.13-disable-broken-sqlite-test.patch

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that
need a programmable interface. This package contains most of the
standard Python modules, as well as modules for interfacing to the
Tix widget set for Tk and RPM.

Note that documentation for Python is provided in the python-docs
package.

%package -n %{libname}
Summary:	Shared libraries for Python %{version}
Group:		System/Libraries
Obsoletes:	%{_lib}python3.3 < 3.3.2-2

%description -n %{libname}
This packages contains Python shared object library.  Python is an
interpreted, interactive, object-oriented programming language often
compared to Tcl, Perl, Scheme or Java.

%package -n %{devname}
Summary:	The libraries and header files needed for Python development
Group:		Development/Python
Requires:	%{name} = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	python-pkg-resources
Provides:	%{name}-devel = %{EVRD}
Provides:	%{name}3-devel = %{EVRD}
Provides:	pkgconfig(python) = 3

%description -n %{devname}
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install %{devname} if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package -n %{staticname}
Summary:	Static libraries needed for Python development
Group:		Development/Python
Requires:	%{devname} = %{EVRD}

%description -n %{staticname}
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install %{staticname} if you want to link statically to Python,
e.g. when using the Nuitka compiler

%package docs
Summary:	Documentation for the Python programming language
Group:		Development/Python
Requires:	%{name} = %{EVRD}
Requires:	xdg-utils
BuildArch:	noarch
Obsoletes:	python3-docs < %{EVRD}

%description docs
The python-docs package contains documentation on the Python
programming language and interpreter.  The documentation is provided
in ASCII text files and in LaTeX source files.

Install the python-docs package if you'd like to use the documentation
for the Python language.

%package ensurepip
Summary:	Python module for installing the pip package manager
Group:		Development/Python
Requires:	%{name} = %{EVRD}

%description ensurepip
Python module for installing the pip package manager

%package -n tkinter
Summary:	A graphical user interface for the Python scripting language
Group:		Development/Python
Requires:	%{name} = %{EVRD}
Requires:	tcl
Requires:	tk
Obsoletes:	tkinter3 < %{EVRD}

%description -n tkinter
The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.

%package -n tkinter-apps
Summary:	Various applications written using tkinter
Group:		Development/Python
Requires:	tkinter = %{EVRD}
Obsoletes:	tkinter3-apps < %{EVRD}

%description -n tkinter-apps
Various applications written using tkinter.

%package test
Summary:	The self-test suite for the main python3 package
Group:		Development/Python
Requires:	%{name} = %{EVRD}

%description test
The self-test suite for the Python interpreter.
This is only useful to test Python itself.

%prep
%autosetup -p1 -n Python-%{version}%{?pre:%{pre}}

# docs
mkdir html
tar xf %{SOURCE1} -C html

find . -type f -print0 | xargs -0 sed -i -e 's@/usr/local/bin/python@%{_bindir}/python@'

cat > README.omv << EOF
Python interpreter support readline completion by default.
This is only used with the interpreter. In order to remove it,
you can :
1) unset PYTHONSTARTUP when you login
2) create a empty file \$HOME/.pythonrc.py
3) change %{_sysconfdir}/pythonrc.py
EOF

# Ensure that internal copies of expat, libffi and zlib are not used.
rm -fr Modules/expat
rm -fr Modules/zlib

%build
# Various violations, including in object.h
# (tpg) https://maskray.me/blog/2021-05-09-fno-semantic-interposition
%global optflags %{optflags} -O2 -fPIC -fno-strict-aliasing -fno-semantic-interposition -Wl,-Bsymbolic
%global build_ldflags %{build_ldflags} -fno-semantic-interposition -Wl,-Bsymbolic

rm -f Modules/Setup.local

# Python's configure adds -std=c11 even for c++, clang doesn't like that
# combination at all
sed -i -e 's,-std=c11,,' configure.ac

# (tpg) Determinism
export PYTHONHASHSEED=0

autoreconf -vfi
# FIXME why is autodetection broken?
export ax_cv_c_float_words_bigendian=no

export CONFIGURE_TOP="$(pwd)"

# to fix curses module build
# https://bugs.mageia.org/show_bug.cgi?id=6702
export OPT="%{optflags} -g"
export CFLAGS="%{optflags} -D_GNU_SOURCE -fPIC -fwrapv -I/usr/include/ncursesw"
export CPPFLAGS="%{optflags} -D_GNU_SOURCE -fPIC -fwrapv -I/usr/include/ncursesw"
export LDFLAGS="${CFLAGS}"

if echo %{__cc} |grep -q clang; then
	LTO=thin
else
	LTO=yes
fi

%if %{cross_compiling}
cat >config.site <<EOF
ac_cv_file__dev_ptmx=yes
ac_cv_file__dev_ptc=no
EOF
export CONFIG_SITE="$(pwd)/config.site ${CONFIG_SITE}"
%endif
mkdir build
cd build
%configure \
	--enable-ipv6 \
	--with-dbmliborder=gdbm \
%if %{with pip}
	--with-ensurepip=install \
%else
	--without-ensurepip \
%endif
	--with-platlibdir=%{_lib} \
	--with-system-expat \
	--with-cxx-main="%{__cxx}" \
	--with-system-ffi \
	--enable-loadable-sqlite-extensions \
	--enable-shared \
	--enable-static \
%if 0
# Disabled for now, since it causes buildtime crashes with llvm 16.0.x
	--enable-bolt \
%endif
%if %{cross_compiling}
	--with-build-python=%{_bindir}/python \
%endif
	--with-lto=$LTO \
	--with-pymalloc \
	--enable-ipv6=yes \
	--with-computed-gotos=yes \
	--with-ssl-default-suites=openssl \
%if %{with valgrind}
	--with-valgrind \
%endif
	--enable-optimizations

# (misc) if the home is nfs mounted, rmdir fails due to delay
export TMP="/tmp" TMPDIR="/tmp"
%ifarch riscv64
# wipe 11 hours of tests
rm -frv Lib/test/test_*
%endif
%make_build PYTHON=python2 -j1

%check
# (misc) if the home is nfs mounted, rmdir fails
export TMP="/tmp" TMPDIR="/tmp"

# Currently (3.3.0-1), LOTS of tests fail, but python3 seems to work
# quite fine anyway. Chances are something in the testsuite itself is bogus.
#make test TESTOPTS="-w -x test_linuxaudiodev -x test_nis -x test_shutil -x test_pyexpat -x test_minidom -x test_sax -x test_string -x test_str -x test_unicode -x test_userstring -x test_bytes -x test_distutils -x test_mailbox -x test_ioctl -x test_telnetlib -x test_strtod -x test_urllib2net -x test_runpy -x test_posix -x test_robotparser -x test_numeric_tower -x test_math -x test_cmath -x test_importlib -x test_import -x test_float -x test_strtod -x test_timeout"

%install
mkdir -p %{buildroot}%{_prefix}/lib/python%{dirver}

# fix Makefile to get rid of reference to distcc
perl -pi -e "/^CC=/ and s|distcc|%{__cc}|" Makefile

# set the install path
echo '[install_scripts]' >setup.cfg
echo 'install_dir='"%{buildroot}%{_bindir}" >>setup.cfg

# python is not GNU and does not know fsstd
mkdir -p %{buildroot}%{_mandir}
%make_install -C build LN="ln -sf"

# Why doesn't the static lib get installed even if it's built?
cp build/libpython%{api}.a %{buildroot}%{_libdir}/

# No .so symlink either...
(cd %{buildroot}%{_libdir}; ln -sf $(ls libpython%{api}*.so.*) libpython%{api}.so)

chmod 755 %{buildroot}%{_bindir}/idle3

%if %{with valgrind}
install Misc/valgrind-python.supp -D %{buildroot}%{_libdir}/valgrind/valgrind-python3.supp
%endif

mkdir -p %{buildroot}%{_datadir}/applications
%if %{with tkinter}
cat > %{buildroot}%{_datadir}/applications/mandriva-tkinter3.desktop << EOF
[Desktop Entry]
Name=IDLE
Comment=IDE for Python3
Exec=%{_bindir}/idle3
Icon=development_environment_section
Terminal=false
Type=Application
Categories=Development;IDE;
EOF
%endif

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-docs.desktop << EOF
[Desktop Entry]
Name=Python documentation
Comment=Python complete reference
Exec=%{_bindir}/xdg-open %{_defaultdocdir}/%{name}-docs/index.html
Icon=documentation_section
Terminal=false
Type=Application
Categories=Documentation;
EOF

# fix non real scripts
#chmod 644 %{buildroot}%{_libdir}/python*/test/test_{binascii,grp,htmlparser}.py*
find %{buildroot} -type f \( -name "test_binascii.py*" -o -name "test_grp.py*" -o -name "test_htmlparser.py*" \) -exec chmod 644 {} \;
# fix python library not stripped
chmod u+w %{buildroot}%{_libdir}/libpython%{api}*.so.1.0 %{buildroot}%{_libdir}/libpython3.so

# drop backup files
#find %{buildroot} -name "*~" -delete
#find . -name "*~" -delete

# Get rid of DOS batch files:
find %{buildroot} -name \*.bat -delete
# Get rid of EXE files:
find %{buildroot} -name \*.exe -delete

%if ! %{with tkinter}
# With tkinter disabled, python's build system is still dumb enough to
# build other parts that rely on tkinter...
# Even the python parts of tkinter itself.
rm -rf \
	%{buildroot}%{_libdir}/python*/{idlelib,tkinter,turtledemo} \
	%{buildroot}%{_bindir}/idle*
%endif

mkdir -p %{buildroot}%{_sysconfdir}/profile.d/

cat > %{buildroot}%{_sysconfdir}/profile.d/30python.sh << 'EOF'
if [ -f $HOME/.pythonrc.py ] ; then
    export PYTHONSTARTUP=$HOME/.pythonrc.py
else
    export PYTHONSTARTUP=/etc/pythonrc.py
fi

export PYTHONDONTWRITEBYTECODE=1
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/30python.csh << 'EOF'
if ( -f ${HOME}/.pythonrc.py ) then
    setenv PYTHONSTARTUP ${HOME}/.pythonrc.py
else
    setenv PYTHONSTARTUP /etc/pythonrc.py
endif
setenv PYTHONDONTWRITEBYTECODE 1
EOF

cat > %{buildroot}%{_sysconfdir}/pythonrc.py << EOF
try:
    # this add completion to python interpreter
    import readline
    import rlcompleter
    # see readline man page for this
    readline.parse_and_bind("set show-all-if-ambiguous on")
    readline.parse_and_bind("tab: complete")
except:
    pass
# you can place a file .pythonrc.py in your home to overrides this one
# but then, this file will not be sourced
EOF

mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d
install -m644 %{S:2} %{buildroot}%{_sysconfdir}/rpm/macros.d/
install -m644 %{S:3} %{buildroot}%{_sysconfdir}/rpm/macros.d/
install -D -m644 %{S:4} %{buildroot}%{_rpmmacrodir}/macros.buildsys.python
# We are the default version...
sed -e 's,python3,python,g;s,py3,py,g' %{SOURCE2} >%{buildroot}%{_sysconfdir}/rpm/macros.d/python.macros

ln -s python3 %{buildroot}%{_bindir}/python
ln -s pydoc3 %{buildroot}%{_bindir}/pydoc
ln -s python3-config %{buildroot}%{_bindir}/python-config

# Fix permissions on docs
find html -type d |xargs chmod 0755
find html -type f |xargs chmod 0644

# Barf if an important module required by dnf didn't build
# (e.g. due to broken dependency libraries)
[ -e %{buildroot}%{_libdir}/python*/lib-dynload/_curses.*.so ] || exit 1
[ -e %{buildroot}%{_libdir}/python*/lib-dynload/_lzma.*.so ] || exit 1
[ -e %{buildroot}%{_libdir}/python*/lib-dynload/_sqlite3.*.so ] || exit 1

%files
%doc README.omv
%{_sysconfdir}/rpm/macros.d/*.macros
%{_rpmmacrodir}/macros.buildsys.python
%{_sysconfdir}/profile.d/*
%config(noreplace) %{_sysconfdir}/pythonrc.py
%{_includedir}/python*/pyconfig.h

%dir %{_libdir}/python*/config-*
%{_libdir}/python*/config*/Makefile
%if %{with tkinter}
%exclude %{_libdir}/python*/lib-dynload/_tkinter.*.so
%endif

# HACK: build fails without this (TODO: investigate rpm)
%dir %{_libdir}/python*
%{_libdir}/python*/LICENSE.txt
%{_libdir}/python%{dirver}/*.py
%{_libdir}/python%{dirver}/__pycache__
%{_libdir}/python%{dirver}/asyncio
%{_libdir}/python%{dirver}/collections
%{_libdir}/python%{dirver}/concurrent
%{_libdir}/python%{dirver}/ctypes
%{_libdir}/python%{dirver}/curses
%{_libdir}/python%{dirver}/dbm
%{_libdir}/python%{dirver}/email
%{_libdir}/python%{dirver}/encodings
%{_libdir}/python%{dirver}/html
%{_libdir}/python%{dirver}/http
%{_libdir}/python%{dirver}/importlib
%{_libdir}/python%{dirver}/json
%{_libdir}/python%{dirver}/lib-dynload
%exclude %{_libdir}/python%{dirver}/lib-dynload/_ctypes_test.*.so
%exclude %{_libdir}/python%{dirver}/lib-dynload/_testbuffer.*.so
%exclude %{_libdir}/python%{dirver}/lib-dynload/_testcapi.*.so
%exclude %{_libdir}/python%{dirver}/lib-dynload/_testimportmultiple.*.so
%{_libdir}/python%{dirver}/logging
%{_libdir}/python%{dirver}/multiprocessing
%{_libdir}/python%{dirver}/pathlib
%{_libdir}/python%{dirver}/__phello__
%{_libdir}/python%{dirver}/_pyrepl
%{_libdir}/python%{dirver}/pydoc_data
%{_libdir}/python%{dirver}/re
%{_libdir}/python%{dirver}/site-packages
%{_libdir}/python%{dirver}/sqlite3
%{_libdir}/python%{dirver}/sysconfig
%{_libdir}/python%{dirver}/tomllib
%{_libdir}/python%{dirver}/unittest
%{_libdir}/python%{dirver}/urllib
%{_libdir}/python%{dirver}/venv
%{_libdir}/python%{dirver}/wsgiref*
%{_libdir}/python%{dirver}/xml
%{_libdir}/python%{dirver}/xmlrpc
%{_libdir}/python%{dirver}/zipfile
%{_libdir}/python%{dirver}/zoneinfo
%{_bindir}/pydoc
%{_bindir}/pydoc3*
%{_bindir}/python
%{_bindir}/python3*
%exclude %{_bindir}/python*config
%if %{with valgrind}
%{_libdir}/valgrind/valgrind-python3.supp
%endif
# pip bits
%if %{with pip}
%if "%{_libdir}" != "%{_prefix}/lib"
# In the %{_libdir} == %{_prefix}/lib case, those are caught by
# globs above.
%dir %{_prefix}/lib/python%{dirver}
%dir %{_prefix}/lib/python%{dirver}/site-packages
%{_prefix}/lib/python%{dirver}/site-packages/__pycache__
%{_prefix}/lib/python%{dirver}/site-packages/pkg_resources.py
%{_prefix}/lib/python%{dirver}/site-packages/easy_install.py
%{_prefix}/lib/python%{dirver}/site-packages/pip
%{_prefix}/lib/python%{dirver}/site-packages/setuptools*
%{_prefix}/lib/python%{dirver}/site-packages/_markerlib
%{_prefix}/lib/python%{dirver}/site-packages/pip-*.dist-info
%endif
%{_bindir}/easy_install-%{dirver}
%{_bindir}/pip3
%{_bindir}/pip%{dirver}
%endif

%files ensurepip
%{_libdir}/python%{dirver}/ensurepip

%files -n %{libname}
%{_libdir}/libpython%{api}.so.%{major}*

%files -n %{devname}
%{_libdir}/libpython*.so
%{_includedir}/python*
%{_libdir}/python*/config-%{dirver}*
%{_bindir}/python-config
%{_bindir}/python%{dirver}*-config
%{_bindir}/python%{familyver}-config
%{_libdir}/pkgconfig/python*.pc
%exclude %{_includedir}/python*/pyconfig.h
%exclude %{_libdir}/python*/config*/Makefile

%files -n %{staticname}
%{_libdir}/libpython*.a

%files docs
%doc html/*/*
%{_datadir}/applications/mandriva-%{name}-docs.desktop
%{_mandir}/man*/*

%if %{with tkinter}
%files -n tkinter
%{_libdir}/python*/tkinter/
%{_libdir}/python%{dirver}/turtledemo
%{_libdir}/python*/idlelib
%{_libdir}/python*/lib-dynload/_tkinter.*.so

%files -n tkinter-apps
%{_bindir}/idle3*
%{_datadir}/applications/mandriva-tkinter3.desktop
%endif

%files test
%{_libdir}/python*/test/
%{_libdir}/python%{dirver}/lib-dynload/_ctypes_test.*.so
%{_libdir}/python%{dirver}/lib-dynload/_testbuffer.*.so
%{_libdir}/python%{dirver}/lib-dynload/_testcapi.*.so
%{_libdir}/python%{dirver}/lib-dynload/_testimportmultiple.*.so
