#
# todo:
# - use XML ISO entities from sgml-common
#
Summary:	XML/SGML DocBook DTD 4.2
Summary(pl):	XML/SGML DocBook DTD 4.2
%define ver	4.3
Name:		docbook-dtd43-xml
Version:	1.0
Release:	4
Vendor:		OASIS
License:	Free
Group:		Applications/Publishing/XML
URL:		http://www.oasis-open.org/docbook/
Source0:	http://www.oasis-open.org/docbook/xml/%{ver}/docbook-xml-%{ver}.zip
# Source0-md5:	ab200202b9e136a144db1e0864c45074
BuildRequires:	libxml2-progs
BuildRequires:	rpm-build >= 4.0.2-94
BuildRequires:	unzip
PreReq:		libxml2
PreReq:		sgml-common
Requires(post,preun):	/usr/bin/install-catalog
Requires(post,preun):	/usr/bin/xmlcatalog
Requires:	libxml2-progs >= 2.4.17-6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dtd_path		%{_datadir}/sgml/docbook/xml-dtd-%{ver}
%define		xmlcat_file		%{dtd_path}/catalog.xml
%define		sgmlcat_file	%{dtd_path}/catalog

%description
DocBook is an XML/SGML vocabulary particularly well suited to books
and papers about computer hardware and software (though it is by no
means limited to only these applications).

%description -l pl
DocBook DTD jest zestawem definicji dokument�w XML/SGML przeznaczonych
do tworzenia dokumentacji technicznej. Stosowany jest do pisania
podr�cznik�w systemowych, instrukcji jak i wielu innych ciekawych
rzeczy.

%prep
%setup -q -c
chmod -R a+rX *

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{dtd_path}

install *.{xml,dtd,mod} $RPM_BUILD_ROOT%{dtd_path}
install *.ent $RPM_BUILD_ROOT%{dtd_path} || :
cp -a ent $RPM_BUILD_ROOT%{dtd_path}

%docbook_sgmlcat_fix $RPM_BUILD_ROOT%{sgmlcat_file} %{ver}

cat docbook.cat >> $RPM_BUILD_ROOT%{sgmlcat_file}

%xmlcat_add_rewrite \
	http://www.oasis-open.org/docbook/xml/%{ver} \
	file://%{dtd_path} \
	$RPM_BUILD_ROOT%{xmlcat_file}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if ! grep -q /etc/sgml/xml-docbook-%{ver}.cat /etc/sgml/catalog ; then
	%sgmlcat_add /etc/sgml/xml-docbook-%{ver}.cat %{sgmlcat_file}

fi
if ! grep -q %{xmlcat_file} /etc/xml/catalog ; then
	%xmlcat_add %{xmlcat_file}

fi

%preun
if [ "$1" = "0" ] ; then
	%sgmlcat_del /etc/sgml/xml-docbook-%{ver}.cat %{sgmlcat_file}
	%xmlcat_del %{xmlcat_file}
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%{dtd_path}
