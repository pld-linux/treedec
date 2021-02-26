#
# Conditional build:
%bcond_with	gala	# use gala graph functions (broken build when using gala snapshot 20181110 + boost 1.70)
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
#
Summary:	Tree decomposition algorithms
Summary(pl.UTF-8):	Algorytmy do rozkładu drzewiastego
Name:		treedec
# configure.ac /AC_INIT
Version:	0.9.0
%define	gitref	aceed466aebd2e9f898172f3a5c3d9f481dfdb63
%define	snap	20181209
%define	rel	4
Release:	1.%{snap}.%{rel}
License:	GPL v2, GPL v3
Group:		Libraries
#Source0Download: https://github.com/freetdi/tdlib/releases
Source0:	https://github.com/freetdi/tdlib/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	dedb02819869f08c1035d23f47883d69
Patch0:		%{name}-python.patch
URL:		https://github.com/freetdi/tdlib
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.55
%{?with_gala:BuildRequires:	freetdi-gala-devel}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2
BuildRequires:	stx-btree-devel
%if %{with python2}
BuildRequires:	python-Cython >= 0.20.0
BuildRequires:	python-devel >= 1:2.7
%endif
%if %{with python3}
BuildRequires:	python3-Cython >= 0.20.0
BuildRequires:	python3-devel >= 1:3.2
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
treedec provides tree decomposition algorithms.

%description -l pl.UTF-8
Biblioteka treedec udostępnia algorytmy rozkładu drzewiastego.

%package devel
Summary:	Tree decomposition algorithms
Summary(pl.UTF-8):	Algorytmy do rozkładu drzewiastego
License:	Boost v1.0
Group:		Development/Libraries
Requires:	libstdc++-devel >= 6:4.7

%description devel
treedec provides tree decomposition algorithms.

%description devel -l pl.UTF-8
Biblioteka treedec udostępnia algorytmy rozkładu drzewiastego.

%package -n python-tdlib
Summary:	Python 2 tree decomposition module
Summary(pl.UTF-8):	Moduł do rozkładu drzewiastego dla Pythona 2
Group:		Libraries/Python

%description -n python-tdlib
Python 2 tree decomposition module.

%description -n python-tdlib -l pl.UTF-8
Moduł do rozkładu drzewiastego dla Pythona 2.

%package -n python3-tdlib
Summary:	Python 3 tree decomposition module
Summary(pl.UTF-8):	Moduł do rozkładu drzewiastego dla Pythona 3
Group:		Libraries/Python

%description -n python3-tdlib
Python 3 tree decomposition module.

%description -n python3-tdlib -l pl.UTF-8
Moduł do rozkładu drzewiastego dla Pythona 3.

%prep
%setup -q -n tdlib-%{gitref}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
install -d build-py2
cd build-py2
../%configure \
	--disable-static \
	%{!?with_gala:--without-gala} \
	--with-python-include-dir=%{py_incdir} \
	%{!?with_python2:--without-python}

%{__make}
cd ..

%if %{with python3}
install -d build-py3
cd build-py3
../%configure \
	PYTHON=%{__python3} \
	--disable-static \
	%{!?with_gala:--without-gala} \
	--with-python-include-dir=%{py3_incdir} \
	%{!?with_python3:--without-python}

%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%{__make} -C build-py3 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/tdlib/cytdlib.la
%endif

%{__make} -C build-py2 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/tdlib/cytdlib.la
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc AUTHORS BUGS COPYING NEWS README THANKS TODO
%{_includedir}/treedec

%if %{with python2}
%files -n python-tdlib
%defattr(644,root,root,755)
%dir %{py_sitedir}/tdlib
%attr(755,root,root) %{py_sitedir}/tdlib/cytdlib.so
%{py_sitedir}/tdlib/*.py[co]
%endif

%if %{with python3}
%files -n python3-tdlib
%defattr(644,root,root,755)
%dir %{py3_sitedir}/tdlib
%attr(755,root,root) %{py3_sitedir}/tdlib/cytdlib.so
%{py3_sitedir}/tdlib/*.py
%{py3_sitedir}/tdlib/__pycache__
%endif
