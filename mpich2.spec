Summary:	MPICH2 Early Release
Summary(pl.UTF-8):	Wczesna wersja MPICH2
Name:		mpich2
Version:	1.4.1p1
Release:	2
License:	BSD-like
Group:		Development/Libraries
Source0:	http://www.mcs.anl.gov/research/projects/mpich2/downloads/tarballs/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b470666749bcb4a0449a072a18e2c204
Patch0:		%{name}-link.patch
Patch1:		%{name}-destdir-fix.patch
Patch2:		%{name}-slog2sdk.patch
URL:		http://www.mcs.anl.gov/research/projects/mpich2
BuildRequires:	gcc-fortran >= 5:4.0
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MPICH2 is an all-new implementation of MPI from the group at Argonne
National Laboratory. It shares many goals with the original MPICH but
no actual code. It is a portable, high-performance implementation of
the entire MPI-2 standard. This release has all MPI-2 functions and
features required by the standard with the exception of support for
the "external32" portable I/O format.

%description -l pl.UTF-8
MPICH2 to całkowicie nowa implementacja MPI wykonana przez grupę z
Argonne National Laboratory. Dzieli wiele idei z oryginalnym MPICH-em,
ale nie sam kod. Jest przenośną, wysoko wydajną implementacją całego
standardu MPI-2. To wydanie zawiera wszystkie funkcje i cechy MPI-2
wymagane przez standard z wyjątkiem obsługi przenośnego formatu I/O
"external32".

%package devel
Summary:        Development files for mpich2
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       gcc-fortran

%description devel
Contains development headers and libraries for mpich2

%package static
Summary:        Static mpich2 libraries
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description static
Static mpich2 libraries.

%package doc
Summary:        Documentations and examples for mpich2
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Contains documentations and examples for mpich2.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1

%build
%configure \
	FC=gfortran \
	F77=gfortran \
	CFLAGS="%{rpmcflags}" \
	CXXFLAGS="%{rpmcxxflags}" \
	FCFLAGS="%{rpmcflags}" \
	FFLAGS="%{rpmcflags}" \
	LDFLAGS="-Wl,--as-needed" \
	MPICH2LIB_CFLAGS="%{rpmcflags}" \
	MPICH2LIB_CXXFLAGS="%{rpmcxxflags}" \
	MPICH2LIB_FCFLAGS="%{rpmcflags}" \
	MPICH2LIB_FFLAGS="%{rpmcflags}" \
	--enable-sharedlibs=gcc \
	--enable-shared \
	--enable-lib-depend \
	--disable-rpath \
	--enable-fc \
	--with-device=ch3:nemesis \
	--with-pm=hydra:gforker \
	--sysconfdir=%{_sysconfdir}/%{name} \
	--includedir=%{_includedir}/%{name} \
	--datadir=%{_datadir}/%{name} \
	--docdir=%{_datadir}/%{name}/doc \
	--htmldir=%{_datadir}/%{name}/doc \
	--with-hwloc-prefix=system \
	--with-java=%{_jvmdir} \

%{__make} -j1 \
	VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/slog2sdk

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT/%{_libdir}/*.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/slog2sdk

# Workaround 1.4.1 broken destdir
for f in mpif77 mpif90 mpicxx mpicc ; do
	%{__sed} -i -e 's#'$RPM_BUILD_ROOT'##' \
		$RPM_BUILD_ROOT%{_bindir}/$f \
		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$f.conf
done

%{__rm} $RPM_BUILD_ROOT%{_sbindir}/mpe*install

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES COPYRIGHT README README.envvar RELEASE_NOTES
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.conf
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.[0-9]
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/slog2sdk
%{_mandir}/man1/*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/mpe_prof.o
%{_includedir}/%{name}
%{_pkgconfigdir}/*.pc
%{_mandir}/man3/*.3*
%{_mandir}/man4/*.4*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files doc
%defattr(644,root,root,755)
%{_datadir}/%{name}/doc
%{_datadir}/%{name}/examples*
%{_datadir}/%{name}/logfiles
