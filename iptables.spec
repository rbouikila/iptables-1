#
# Conditional build:
%bcond_without	doc		# without documentation (HOWTOS) which needed TeX
%bcond_without	dist_kernel	# without distribution kernel
#
%define		netfilter_snap		20040518
%define		iptables_version	1.2.10
%define		llh_version		7:2.6.5.1-6
#
Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl):	System filtrowania pakiet�w oraz system translacji adres�w (NAT)
Summary(pt_BR):	Ferramenta para controlar a filtragem de pacotes no kernel-2.4.x
Summary(ru):	������� ��� ���������� ��������� ��������� ���� Linux
Summary(uk):	���̦�� ��� ��������� ��������� Ʀ������� ���� Linux
Summary(zh_CN):	Linux�ں˰����˹�������
Name:		iptables
%if %{netfilter_snap} != 0
Version:	%{iptables_version}_%{netfilter_snap}
%else
Version:	%{iptables_version}
%endif
%define		_rel	2
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Networking/Daemons
URL:		http://www.netfilter.org/
Vendor:		Netfilter mailing list <netfilter@lists.samba.org>
%if %{netfilter_snap} != 0
Source0:	%{name}-%{iptables_version}_%{netfilter_snap}.tar.bz2
%else
Source0:	http://www.netfilter.org/files/%{name}-%{version}.tar.bz2
%endif
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
# Source1-md5:	2ed2b452daefe70ededd75dc0061fd07
Source2:	%{name}.init
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-1.2.9-ipt_imq.patch
%if %{with doc}
BuildRequires:	sgml-tools
BuildRequires:	sgmls
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
BuildRequires:	tetex-tex-babel
%endif
BuildRequires:	sed >= 4.0
%if %{with dist_kernel} && %{netfilter_snap} != 0
BuildRequires:	kernel-headers(netfilter) = %{netfilter_snap}
BuildRequires:	kernel-source
Requires:	kernel(netfilter) = %{netfilter_snap}
%endif
BuildRequires:	linux-libc-headers >= %{llh_version}
BuildConflicts:	kernel-headers < 2.3.0
Provides:	firewall-userspace-tool
Obsoletes:	netfilter
Obsoletes:	ipchains
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	%{name} = %{version}-%{release}

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl
Biblioteki i pliki nag��wkowe niezb�dne do tworzenia rozszerze� dla
iptables.

%package init
Summary:	Iptables init (RedHat style)
Summary(pl):	Iptables init (w stylu RedHata)
Group:		Networking/Admin
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}
Obsoletes:	firewall-init
Obsoletes:	firewall-init-ipchains

%description init
Iptables-init is meant to provide an alternate way than firewall-init
to start and stop packet filtering through iptables(8).

%description init -l pl
Iptables-init ma na celu udost�pnienie alternatywnego w stosunku do
firewall-init sposobu w��czania i wy��czania filtr�w IP j�dra poprzez
iptables(8).

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1

# removed broken ...
#%rm -f extensions/.set-test

chmod 755 extensions/.*-test*
sed -i 's:$(HTML_HOWTOS)::g; s:$(PSUS_HOWTOS)::g' iptables-howtos/Makefile

%build
%{__make} all experimental \
	CC="%{__cc}" \
	COPT_FLAGS="%{rpmcflags} -D%{!?debug:N}DEBUG" \
	KERNEL_DIR="%{_kernelsrcdir}" \
	LIBDIR="%{_libdir}"

%{?with_doc:%{__make} -C iptables-howtos}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_initrddir},%{_includedir},%{_libdir},%{_mandir}/man3,}

echo ".so iptables-save.8" > ip6tables-save.8
echo ".so iptables-restore.8" > ip6tables-restore.8

%{__make} install install-experimental \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

echo ".so iptables.8" > $RPM_BUILD_ROOT%{_mandir}/man8/ip6tables.8

# Devel stuff
cp -a include/{lib*,ip*} $RPM_BUILD_ROOT%{_includedir}
install lib*/lib*.a $RPM_BUILD_ROOT%{_libdir}
install libipq/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

install %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/iptables

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add %{name}

%preun init
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%{?with_doc:%doc iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*}
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/iptables
%attr(755,root,root) %{_libdir}/iptables/*.so
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%{?with_doc:%doc iptables-howtos/netfilter-hacking-HOWTO*}
%{_libdir}/lib*.a
%{_includedir}/*.h
%dir %{_includedir}/libip*
%{_includedir}/libip*/*.h
%{_mandir}/man3/*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) %{_initrddir}/iptables
