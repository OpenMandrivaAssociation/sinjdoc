
%define gcj_support 1
%bcond_with	bootstrap

%if %with bootstrap
%define gcj_support 0
%endif

Name:           sinjdoc
Version:        0.5
Release:        %mkrel 4.3
Summary:        Documentation generator for Java source code
Group:          Development/Java
License:        GPL
URL:            http://www.cag.lcs.mit.edu/~cananian/Projects/GJ/sinjdoc-latest/
Source0:        %name-%version.tar.bz2
Patch0:         sinjdoc-annotations.patch
Patch1:         sinjdoc-autotools-changes.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%if %without bootstrap
BuildRequires:	eclipse-ecj
%else
BuildRequires:	ecj-bootstrap
%endif

BuildRequires:	java_cup >= 0.10
BuildRequires:	java
BuildRequires:	jpackage-utils
BuildRequires:  java-gcj-compat-devel
Requires:       java_cup >= 0.10
Requires:	java
Requires:	jpackage-utils

%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
%else
BuildArch:      noarch
%endif

# (anssi) do not obsolete yet
#Obsoletes: gjdoc <= 0.7.7-14.fc7

%description
This package contains Sinjdoc a tool for generating Javadoc-style
documentation from Java source code

%prep
%setup -q
%patch0 -p0
%patch1 -p0
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
rm -rf $RPM_BUILD_ROOT

%jpackage_script net.cscott.sinjdoc.Main %{nil} %{nil} %{name}:java_cup-runtime %{name}

chmod a+x %{buildroot}%{_bindir}/sinjdoc

install -d 755 $RPM_BUILD_ROOT%{_javadir}
install -D -m 644 sinjdoc.jar $RPM_BUILD_ROOT%{_javadir}/sinjdoc.jar

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

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
