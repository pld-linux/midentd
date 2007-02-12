%include	/usr/lib/rpm/macros.perl
Summary:	Ident server with masquerading support
Summary(pl.UTF-8):   Ident serwer z obsługą maskowanych adresów IP
Name:		midentd
Version:	2.3.1
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	http://panorama.sth.ac.at/midentd/files/%{name}-%{version}.tar.gz
# Source0-md5:	84aca797c2569667a52fa9f5d4ac3e21
Source1:	%{name}.inetd
Source2:	%{name}.logrotate
URL:		http://panorama.sth.ac.at/midentd/
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	rc-inetd
Provides:	identserver
Obsoletes:	linux-identd
Obsoletes:	linux-identd-inetd
Obsoletes:	linux-identd-standalone
Obsoletes:	oidentd
Obsoletes:	oidentd-inetd
Obsoletes:	oidentd-standalone
Obsoletes:	pidentd
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
midentd is an identd replacement with masquerading support. With your
average identd on a masquerading firewall, if an ident request comes
in for a masqueraded connection, it will return 'ERROR : NO-USER' or
something along those lines. This may be quite irritating at times,
with, for example, IRC servers that won't let you in if they don't get
a valid ident reply.

%description -l pl.UTF-8
midentd jest serwerem usługi ident z obsługą maskowania adresów.
Jeżeli masz zainstalowanego zwykłego identd oraz korzystasz z
maskowania adresów przy zapytaniu o maskowane połączenie identd zwraca
'ERROR : NO-USER' lub coś w tym stylu. To może być czasami irytujące,
na przykład jak serwery IRC-a nie chcą Cię wpuścić jeżeli nie
otrzymają poprawnej odpowiedzi o ident.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/sysconfig/rc-inetd,/etc/logrotate.d,%{_sbindir},/var/log}

install midentd $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/midentd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/midentd

:> $RPM_BUILD_ROOT%{_sysconfdir}/midentd.conf
:> $RPM_BUILD_ROOT%{_sysconfdir}/midentd.mircusers
:> $RPM_BUILD_ROOT/var/log/midentd.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q rc-inetd reload

%postun
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/midentd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/midentd.*
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/midentd
%attr(600,nobody,root) %ghost /var/log/midentd.log # FIXME nobody user/group can't own files! -adapter.awk
