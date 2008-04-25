Name:           epel-release       
Version:        4 
Release:        9
Summary:        Extra Packages for Enterprise Linux repository configuration

Group:          System Environment/Base 
License:        GPL 
URL:            http://download.fedoraproject.org/pub/epel

# This is a Fedora maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.

Source0:        http://download.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL
Source1:        GPL	
Source2:        epel.repo	
Source3:        epel-testing.repo	

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch
Requires:      redhat-release >=  %{version} 
Requires(postun): perl
Requires(post): perl

%description
This package contains the Extra Packages for Enterprise Linux (EPEL) repository
GPG key as well as configuration for yum and up2date.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .
install -pm 644 %{SOURCE1} .

%build


%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
install -Dpm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2} %{SOURCE3}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
RHN_SOURCES=/etc/sysconfig/rhn/sources
if [ -e ${RHN_SOURCES} ]; then
  if ! grep -q "^#DONT UPDATE %{name}" ${RHN_SOURCES} > /dev/null 2>&1; then
    # remove existing config
    perl -n -i -e 'print if not /^#BEGIN %{name}/ ... /^#END %{name}/' ${RHN_SOURCES}

    # add updated config unless user specifies not to
    echo "#BEGIN %{name}" >> ${RHN_SOURCES}
    echo "# This block is managed by the %{name} RPM." >> ${RHN_SOURCES}
    echo "" >> ${RHN_SOURCES}
    echo "yum EPEL http://download.fedoraproject.org/pub/epel/%{version}/\$ARCH" >> ${RHN_SOURCES}
    echo "" >> ${RHN_SOURCES}
    echo "#END %{name}" >> ${RHN_SOURCES}
  fi
fi
exit 0

%postun 
RHN_SOURCES=/etc/sysconfig/rhn/sources
if [ $1 = 0 ]; then 
 # remove up2date config here
  if [ -e $RHN_SOURCES ]; then
    perl -n -i -e 'print if not /^#BEGIN %{name}/ ... /^#END %{name}/' ${RHN_SOURCES}
  fi
fi
exit 0


%files
%defattr(-,root,root,-)
%doc GPL
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*


%changelog
* Fri Apr 25 2008 Matt Domsch <Matt_Domsch@dell.com> - 4-9
- fix post and postun.  postun would unconditionally remove the lines
  added by post.

* Fri Apr 25 2008 Matt Domsch <Matt_Domsch@dell.com> - 4-8
- use mirrorlists in epel-testing.repo
- use download.fedoraproject.org in (commented out) baseurls

* Fri Apr 25 2008 Michael Stahnke <mastahnke@gmail.com> - 4-7
- Updated the repo file to use mirror manager for yum 

* Sun Mar 25 2007 Michael Stahnke <mastahnke@gmail.com> - 4-6
- Hard-coded '4' in yum repo files to fix string mismatch. 

* Sun Mar 25 2007 Michael Stahnke <mastahnke@gmail.com> - 4-5
- Specfile cleanup

* Sun Mar 25 2007 Michael Stahnke <mastahnke@gmail.com> - 4-4
- Changed description again

* Sun Mar 25 2007 Michael Stahnke <mastahnke@gmail.com> - 4-3
- Removed cp in postun
- Removed the file epel-release - provides no value
- Removed dist tag as per review bug #233236
- Changed description

* Mon Mar 14 2007 Michael Stahnke <mastahnke@gmail.com> - 4-2
- Fixed up2date issues. 

* Mon Mar 12 2007 Michael Stahnke <mastahnke@gmail.com> - 4-1
- Initial Package
