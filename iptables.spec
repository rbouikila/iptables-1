#
# Conditional build:
# _without_patchedkernel - without ippool, prestate, log (which requires patched 2.4.x kernel)
#
Summary:	extensible packet filtering system && extensible NAT system
Summary(pl):	system filtrowania pakiet�w oraz system translacji adres�w (NAT)
Name:		iptables
Version:	1.2.3
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
URL:		http://netfilter.samba.org/
Vendor:		Netfilter mailing list <netfilter@lists.samba.org>
Source0:	http://netfilter.samba.org/%{name}-%{version}.tar.bz2
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
Patch0:		%{name}-man.patch
Patch1:		%{name}-NETMAP-fix.patch
Patch2:		%{name}-log.patch
Patch3:		%{name}-prestate.patch
BuildRequires:	sgml-tools
BuildRequires:	sgmls
BuildRequires:	tetex-latex
BuildRequires:	tetex-dvips
#Requires:	kernel >= 2.4.2-2
Obsoletes:	netfilter
Obsoletes:	ipchains
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
An extensible NAT system, and an extensible packet filtering system.
Replacement of ipchains in 2.4 kernels.

%description -l pl
Wydajny system translacji adres�w (NAT) oraz system filtrowania
pakiet�w. Zamiennik ipchains w j�drach 2.4

%package devel
Summary:	Libraries and headers for developing iptables extensions
Summary(pl):	Biblioteki i nag��wki do tworzenia rozszerze� iptables
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl
Biblioteki i pliki nag��wkowe niezb�dne do tworzenia rozszerze� dla
iptables.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%{!?_without_patchedkernel:%patch2 -p1}
%{!?_without_patchedkernel:%patch3 -p1}
chmod 755 extensions/.*-test*
mv -f extensions/.NETLINK.test extensions/.NETLINK-test
perl -pi -e 's/\$\(HTML_HOWTOS\)//g; s/\$\(PSUS_HOWTOS\)//g' iptables-howtos/Makefile

%build
%{__make} depend 2> /dev/null || :
%{__make} COPT_FLAGS="%{rpmcflags}" \
	LIBDIR="%{_libdir}" \
	all experimental

%{__make} -C iptables-howtos

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/iptables,%{_mandir}/man3}

echo ".so iptables-save.8" > ip6tables-save.8
echo ".so iptables-restore.8" > ip6tables-restore.8

%{__make} install install-experimental \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

echo ".so iptables.8" > $RPM_BUILD_ROOT%{_mandir}/man8/ip6tables.8

# Devel stuff
cp -a include/* $RPM_BUILD_ROOT%{_includedir}/iptables
install lib*/lib*.a $RPM_BUILD_ROOT%{_libdir}
install libipq/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

%{!?_without_patchedkernel:install ippool/lib*.a $RPM_BUILD_ROOT%{_libdir}}
%{!?_without_patchedkernel:install ippool/ippool $RPM_BUILD_ROOT%{_sbindir}}

gzip -9nf KNOWN_BUGS iptables-howtos/*.{txt,ps}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc KNOWN_BUGS.gz
%doc iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*.gz

%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/iptables/*.so

%{_mandir}/man*/*

%files devel
%defattr(644,root,root,755)
%doc iptables-howtos/netfilter-hacking-HOWTO*.gz
%{_libdir}/lib*.a
%{_includedir}/iptables
%{_mandir}/man3/*
