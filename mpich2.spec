Summary:	MPICH2 Early Release
Summary(pl.UTF-8):	Wczesna wersja MPICH2
Name:		mpich2
Version:	1.0.5p4
Release:	0.1
License:	BSD-like
Group:		Development/Libraries
Source0:	ftp://ftp.mcs.anl.gov/pub/mpi/%{name}-%{version}.tar.gz
# Source0-md5:	d8e0dacdd4ca5ef57a598891989ed409
URL:		http://www-unix.mcs.anl.gov/mpi/
BuildRequires:	gcc-fortran >= 5:4.0
BuildRequires:	libstdc++-devel
Requires:	python >= 2.2
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

%prep
%setup -q

%build
%configure \
	F90FLAGS="%{rpmcflags}" \
	--enable-f77 \
	--enable-f90 \
	--enable-cxx

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# missing in make install
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,3}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_prefix}/{doc,www}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES COPYRIGHT README{,.romio,.testing} doc/{logging,smpd,userguide}/*.pdf
# doc/refman/mpiman.pdf
%attr(755,root,root) %{_bindir}/*
%{_libdir}/lib*.a
%{_libdir}/mpe_prof.o
%{_includedir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
