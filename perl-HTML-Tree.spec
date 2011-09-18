Name:           perl-HTML-Tree
Version:        3.23
Release:        10%{?dist}
Summary:        HTML tree handling modules for Perl
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/HTML-Tree/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PETEK/HTML-Tree-%{version}.tar.gz
# Upstream bug filed:
# https://rt.cpan.org/Ticket/Display.html?id=49932
Patch0:         missing_close_tag.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(HTML::Parser) >= 2.19
BuildRequires:  perl(HTML::Tagset) >= 3.02
# For improved tests
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::More)
Epoch:		1
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This distribution contains a suite of modules for representing,
creating, and extracting information from HTML syntax trees; there is
also relevent documentation.  These modules used to be part of the
libwww-perl distribution, but are now unbundled in order to facilitate
a separate development track.

%prep
%setup -q -n HTML-Tree-%{version}
%patch0 -p1 -b .missing-close-tag
%{__perl} -pi -e 's|/usr/local/bin/perl|%{__perl}|' htmltree

cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
    sed -e '/^perl(main)$/d'
EOF
%define __perl_provides %{_builddir}/HTML-Tree-%{version}/%{name}-prov
chmod +x %{__perl_provides}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README TODO htmltree
%{perl_vendorlib}/HTML
%{_mandir}/man3/HTML::*3*

%changelog
* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:3.23-10
- rebuild against perl 5.10.1

* Mon Sep 28 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.23-9
- apply Jeff Fearn's fix for the missing close tag bug (bz 535587)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.23-5
- fix source url

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.23-4
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.23-3
- rebuild for new perl

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.23-2
- license tag fix

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.23-1
- bump to 3.23

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.21-1
- bump to 3.21

* Tue Jul 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.20-2
- bump epoch to ensure clean upgrades

* Fri Jul  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.20-1
- bump to 3.20

* Mon Jan 16 2006 Ralf Corsépius <rc040203@freenet.de> - 3.1901-2
- BR: perl(Test::Pod).

* Mon Jan 16 2006 Ralf Corsépius <rc040203@freenet.de> - 3.1901-1
- Spec cleanup.
- Filter Provides: perl(main).
- Upstream update.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Jan  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:3.18-2
- Don't install htmltree into %%{_bindir} but include it in docs.

* Sat Dec  4 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.18-0.fdr.1
- First build.
