%include	/usr/lib/rpm/macros.perl
Summary:	Ident server with masquerading support
Summary(pl):	Ident serwer z obs³ug± maskowanych adresów IP
Name:		midentd
Version:	2.3.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://panorama.sth.ac.at/midentd/files/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.logrotate
URL:		http://panorama.sth.ac.at/midentd/
BuildRequires:	perl-devel
Prereq:		rc-inetd
Provides:	identserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Buildarch:	noarch
Obsoletes:	pidentd
Obsoletes:	oidentd

%description
midentd is an identd replacement with masquerading support. With your
average identd on a masquerading firewall, if an ident request comes
in for a masqueraded connection, it will return 'ERROR : NO-USER' or
something along those lines. This may be quite irritating at times,
with, for example, IRC servers that won't let you in if they don't get
a valid ident reply.

%description -l pl
midentd jest serwerem us³ugi ident z obs³ug± maskowania adresów.
Je¿eli masz zainstalowanego zwyk³ego identd oraz korzystasz z
maskowania adresów przy zapytaniu o maskowane po³±czenie identd zwraca
'ERROR : NO-USER' kyb co¶ w tym stylu. To mo¿e byæ czasami irytuj±ce,
na przyk³ad jak serwery IRC-a nie chc± Ciê wpu¶ciæ je¿eli nie
otrzymaj± poprawnej odpowiedzi o ident.

%prep
%setup  -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/sysconfig/rc-inetd,/etc/logrotate.d,%{_sbindir},/var/log}

install midentd $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/midentd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/midentd

gzip -9nf CHANGELOG README
:> $RPM_BUILD_ROOT%{_sysconfdir}/midentd.conf
:> $RPM_BUILD_ROOT%{_sysconfdir}/midentd.mircusers
:> $RPM_BUILD_ROOT/var/log/midentd.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
        /etc/rc.d/init.d/rc-inetd reload 1>&2
else
        echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
        /etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/sysconfig/rc-inetd/midentd
%config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/midentd.*
%attr(755,root,root) %{_sbindir}/*
%config /etc/logrotate.d/midentd
%attr(0600,nobody,root) %ghost /var/log/midentd.log
