Summary:	MPICH2 Early Release
Summary(pl):	Wczesna wersja MPICH2
Name:		mpich2
Version:	0.94
Release:	0.1
License:	BSD-like
Group:		Development/Libraries
Source0:	ftp://ftp.mcs.anl.gov/pub/mpi/%{name}-%{version}.tar.gz
# Source0-md5:	6cfa35fd49a31c8f858d69881921f28b
URL:		http://www-unix.mcs.anl.gov/mpi/
BuildRequires:	gcc-g77
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains an early release of MPICH2. It has been tested
by authors in their own environment, but not extensively tested by
outside users (This is where you come in!). If you are interested in
what the next generation of MPICH will look like, or for helping
harden this version for wider distribution, this package is for you.
If you are looking for an implementation of MPI for use in building
and running your favorite application(s), please obtain the MPICH
1.2.X.

%description -l pl
Ten pakiet zawiera wczesn± wersjê MPICH2. Jest testowana przez autorów
w ich ¶rodowisku, ale nie by³a jeszcze dostatecznie testowana przez
u¿ytkowników zewnêtrznych. Ten pakiet jest dla zainteresowanych, jak
bêdzie wygl±da³ MPICH nowej generacji oraz tym, którzy chc± pomóc w
stabilizowaniu tej wersji do szerszej dystrybucji. Do zastosowañ
produkcyjnych i innych wymagaj±cych stabilno¶ci nale¿y u¿ywaæ pakietu
MPICH 1.2.X.

%prep
%setup -q

%build
%configure2_13 \
	--enable-sharedlibs=gcc \
	--enable-f77 \
	--enable-cxx

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	includedir=$RPM_BUILD_ROOT%{_includedir} \
	exec_prefix=$RPM_BUILD_ROOT%{_exec_prefix} \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir}

# install-docs is broken, so install manuals manually
install -d $RPM_BUILD_ROOT%{_mandir}/man3
install man/man3/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES COPYRIGHT README{,.romio,.testing} doc/*/*.ps
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_includedir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
%{_mandir}/man3/*.3*
