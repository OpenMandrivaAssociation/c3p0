%_javapackages_macros
Name:    c3p0
Version: 0.9.2.1
Release: 4.0%{?dist}
Summary: JDBC DataSources/Resource Pools
License: LGPLv2 or EPL
URL:     https://github.com/swaldman/c3p0


BuildRequires: java-devel >= 1:1.6.0
BuildRequires: java-javadoc >= 1:1.6.0
BuildRequires: jpackage-utils
BuildRequires: ant
BuildRequires: mchange-commons >= 0.2.3.4

Requires: java
Requires: mchange-commons >= 0.2.3.4
Requires: jpackage-utils

Source0: https://github.com/swaldman/%{name}/archive/%{name}-%{version}-final.tar.gz

# Patch to build on java 1.6
Patch0: %{name}-build-on-1.6.patch

# Patch to build on java 1.7 (intentionally kept separate from above)
Patch1: %{name}-build-on-1.7.patch

BuildArch: noarch

%description
c3p0 is an easy-to-use library for augmenting traditional JDBC drivers with
JNDI-bindable DataSources, including DataSources that implement Connection
and Statement Pooling, as described by the jdbc3 spec and jdbc2 standard
extension.

%package  javadoc
Summary:  API documentation for %{name}

Requires: jpackage-utils

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{name}-%{version}-final

%patch0 -p1 -b .java6
%patch1 -p1 -b .java7

# remove all binary bits
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

# remove manifest classpath
sed -i.bak -e "s/<attribute\ name=\"Class-Path\"\ value=\"\${mchange-commons-java\.jar\.file\.name}\"\ \/>//" build.xml

%build
ant \
  -Dbuild.sysclasspath=first \
  -Dmchange-commons-java.jar.file=`build-classpath mchange-commons-java` \
  jar javadoc

sed -i -e "s|@c3p0.version.maven@|%{version}|g" \
  -e "s|@mchange-commons-java.version.maven@|0.2.3.4|g" \
  src/maven/pom.xml

%install
# jar
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 build/%{name}-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}.jar

# javadocs
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr build/apidocs/* %{buildroot}%{_javadocdir}/%{name}

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 src/maven/pom.xml \
  %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap -a "c3p0:c3p0" JPP-%{name}.pom %{name}.jar

%files
%doc src/dist-static/CHANGELOG
%doc src/dist-static/LICENSE*
%doc src/dist-static/RELEASE*
%doc src/doc/index.html
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-*
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc src/dist-static/LICENSE*
%{_javadocdir}/%{name}
