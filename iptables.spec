#
# Conditional build:
# _with_patchedkernel - with ippool, prestate, log (which requires patched 2.4.x kernel)
#
Summary:	extensible packet filtering system && extensible NAT system
Summary(pl):	system filtrowania pakiet�w oraz system translacji adres�w (NAT)
Summary(pt_BR):	Ferramenta para controlar a filtragem de pacotes no kernel-2.4.x
Summary(ru):	������� ��� ���������� ��������� ��������� ���� Linux
Summary(uk):	���̦�� ��� ��������� ��������� Ʀ������� ���� Linux
Summary(zh_CN):	Linux�ں˰����˹�������
Name:		iptables
Version:	1.2.7a
Release:	1
License:	GPL
Group:		Networking/Daemons
URL:		http://www.netfilter.org/
Vendor:		Netfilter mailing list <netfilter@lists.samba.org>
Source0:	http://www.netfilter.org/files/%{name}-%{version}.tar.bz2
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
Patch0:		%{name}-man.patch
Patch1:		%{name}-log.patch
Patch2:		%{name}-prestate.patch
BuildRequires:	perl
BuildRequires:	sgml-tools
BuildRequires:	sgmls
BuildRequires:	tetex-latex
BuildRequires:	tetex-dvips
BuildConflicts:	kernel-headers < 2.3.0
Obsoletes:	netfilter
Obsoletes:	ipchains
Provides:	firewall-userspace-tool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
An extensible NAT system, and an extensible packet filtering system.
Replacement of ipchains in 2.4 kernels.

%description -l pl
Wydajny system translacji adres�w (NAT) oraz system filtrowania
pakiet�w. Zamiennik ipchains w j�drach 2.4

%description -l pt_BR
Esta � a ferramenta que controla o c�digo de filtragem de pacotes do
kernel 2.4, obsoletando ipchains. Com esta ferramenta voc� pode
configurar filtros de pacotes, NAT, mascaramento (masquerading),
regras din�micas (stateful inspection), etc.

%description -l ru
iptables ��������� ����� ���������� ������� ������� � ���� Linux. ���
��������� ��� ������������� ���������� ������ (firewalls) � IP
�����������, � �.�.

%description -l uk
iptables ���������� ����� Ʀ�����æ� ����Ԧ� ����֦ � ��Ҧ Linux. ����
���������� ��� ������������� ͦ�������צ ������ (firewalls) �� IP
�����������, ����.

%package devel
Summary:	Libraries and headers for developing iptables extensions
Summary(pl):	Biblioteki i nag��wki do tworzenia rozszerze� iptables
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl
Biblioteki i pliki nag��wkowe niezb�dne do tworzenia rozszerze� dla
iptables.

%prep
%setup -q -a1
%patch0 -p1
%{?_with_patchedkernel:%patch1 -p1}
%{?_with_patchedkernel:%patch2 -p1}

chmod 755 extensions/.*-test*
mv -f extensions/.NETLINK.test extensions/.NETLINK-test
perl -pi -e 's/\$\(HTML_HOWTOS\)//g; s/\$\(PSUS_HOWTOS\)//g' iptables-howtos/Makefile

%build
%{__make} depend 2> /dev/null || :
%{__make} CC="%{__cc}" \
	COPT_FLAGS="%{rpmcflags} -D%{!?debug:N}DEBUG" \
	LIBDIR="%{_libdir}" \
	all experimental

echo 'all : $(TXT_HOWTOS)  $(HTML_HOWTOS)' >> iptables-howtos/Makefile
%{__make} all -C iptables-howtos

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

#%{?_with_patchedkernel:install ippool/lib*.a $RPM_BUILD_ROOT%{_libdir}}
#%{?_with_patchedkernel:install ippool/ippool $RPM_BUILD_ROOT%{_sbindir}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc KNOWN_BUGS
%doc iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*

%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/iptables
%attr(755,root,root) %{_libdir}/iptables/*.so

%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%doc iptables-howtos/netfilter-hacking-HOWTO*
%{_libdir}/lib*.a
%{_includedir}/iptables
%{_mandir}/man3/*
