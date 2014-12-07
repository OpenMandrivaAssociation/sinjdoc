
%define gcj_support 0
%bcond_with        bootstrap

%if %with bootstrap
%define gcj_support 0
%endif

Name:           sinjdoc
Version:        0.5
Release:        4.17
Summary:        Documentation generator for Java source code
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:        GPL
URL:            http://www.cag.lcs.mit.edu/~cananian/Projects/GJ/sinjdoc-latest/
Source0:        %name-%version.tar.bz2
Patch0:         sinjdoc-annotations.patch
Patch1:         sinjdoc-autotools-changes.patch
Patch2:         sinjdoc-0.5-doclet.patch

%if %without bootstrap
BuildRequires:  eclipse-ecj
%else
BuildRequires:  ecj-bootstrap
%endif

BuildRequires:  java_cup >= 0.10
BuildRequires:  java
BuildRequires:  java-rpmbuild
BuildRequires:  java-gcj-compat-devel
Requires:       java_cup >= 0.10
Requires:       java
Requires:       jpackage-utils

%if !%{gcj_support}
BuildArch:      noarch
%endif

# (anssi) do not obsolete yet
#Obsoletes:     gjdoc <= 0.7.7-14.fc7

%description
This package contains Sinjdoc a tool for generating Javadoc-style
documentation from Java source code

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1
%{__perl} -pi -e 's|javac|%{javac}|' configure.ac
%{__aclocal}
%{__automake}
%{__autoconf}

%build
export JAR=%{jar}
export JAVA=%{java}

%if %with bootstrap
# (anssi) run ecj with libgcj9 instead of libgcj7 (libgcj8 could work as well)
export LD_LIBRARY_PATH=%{_libdir}/gcj_bc-4.3:$LD_LIBRARY_PATH
%endif

%{configure2_5x}
%{make}

%install
rm -rf %{buildroot}

%jpackage_script net.cscott.sinjdoc.Main %{nil} %{nil} %{name}:java_cup-runtime %{name}

chmod a+x %{buildroot}%{_bindir}/sinjdoc

install -d 755 %{buildroot}%{_javadir}
install -D -m 644 sinjdoc.jar %{buildroot}%{_javadir}/sinjdoc.jar

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}
%endif

%if %{gcj_support}
%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING README
%attr(0755,root,root) %{_bindir}/sinjdoc
%{_javadir}/sinjdoc.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.5-4.10mdv2011.0
+ Revision: 669981
- mass rebuild

* Wed Feb 16 2011 Paulo Andrade <pcpa@mandriva.com.br> 0.5-4.9
+ Revision: 638011
- Rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5-4.8mdv2011.0
+ Revision: 607538
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5-4.7mdv2010.1
+ Revision: 524076
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.5-4.6mdv2010.0
+ Revision: 427141
- rebuild

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 0.5-4.5mdv2009.0
+ Revision: 168245
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0.5-4.5mdv2008.1
+ Revision: 121022
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0.5-4.4mdv2008.0
+ Revision: 87362
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

  + David Walluck <walluck@mandriva.org>
    - replace tabs with spaces
    - use macro for %%{buildroot}
    - use more standard buildroot
    - search for javac before ecj, and use correct javac
    - call autotools in %%prep, not %%build
    - set JAR and JAVA to correct values before calling configure
    - stricter permissions in %%files

* Fri Jun 29 2007 Anssi Hannula <anssi@mandriva.org> 0.5-4.2mdv2008.0
+ Revision: 45789
- disable bootstrap

* Wed Jun 27 2007 Anssi Hannula <anssi@mandriva.org> 0.5-4.1mdv2008.0
+ Revision: 44804
- initial Mandriva release

