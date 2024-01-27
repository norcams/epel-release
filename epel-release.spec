Name:           epel-release
Version:        8
Release:        19%{dist}
Summary:        Extra Packages for Enterprise Linux repository configuration

License:        GPLv2

# This is a EPEL maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
URL:            http://download.fedoraproject.org/pub/epel
Source0:        http://download.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-8
Source1:        GPL
Source2:        README-epel-8-packaging.md
# EPEL default preset policy (borrowed from fedora's 90-default.preset)
Source3:        90-epel.preset


Source100:      epel.repo

# Add epel crb repo
Source301:      crb

BuildArch:     noarch
Requires:      redhat-release >=  %{version}
# epel-release is only for enterprise linux, not fedora
Conflicts:     fedora-release
# crb needs config-manager to run
# But only recommend it, incase people do not need crb
Recommends:    dnf-command(config-manager)
Recommends:    (epel-next-release if centos-stream-release)


%description
This package contains the Extra Packages for Enterprise Linux (EPEL) repository
GPG key as well as configuration for yum.


%prep
%setup -q  -c -T
install -pm 644 %{SOURCE1} .
install -pm 644 %{SOURCE2} .


%install
#GPG Key
install -Dpm 644 %{SOURCE0} \
    %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL-%{version}

# yum
install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE100} %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 -D %{SOURCE3} %{buildroot}%{_prefix}/lib/systemd/system-preset/90-epel.preset

# Add epel crb repo
install -D -pm744 -t %{buildroot}%{_bindir} %{SOURCE301}

%post
# Doing a check to see if crb is enabled is as hard and resource intense as enabling or disabling crb.
#   So we will say crb is recommended, without first checking.  But only on the initial install.
if [ "$1" -eq 1 ] ; then
  echo "Many EPEL packages require the CodeReady Builder (CRB) repository."
  echo "It is recommended that you run %{_bindir}/crb enable to enable the CRB repository."
fi


%files
%doc README-epel-8-packaging.md
%license GPL
%config(noreplace) %{_sysconfdir}/yum.repos.d/epel.repo
%{_sysconfdir}/pki/rpm-gpg/*
%{_prefix}/lib/systemd/system-preset/90-epel.preset
%{_bindir}/crb


%changelog
* Mon Apr 17 2023 Troy Dawson <tdawson@redhat.com> - 8-19
- Tweak crb script, check os-release for RHEL (#2186721)

* Thu Sep 29 2022 Carl George <carl@george.computer> - 8-18
- Disable epel-modular repo by default
- Mark all epel-modular repos as deprecated

* Tue Aug 09 2022 Troy Dawson <tdawson@redhat.com> - 8-17
- Tweak crb script, Recommends dnf-command(config-manager) (#2115602)

* Thu Jun 30 2022 Troy Dawson <tdawson@redhat.com> - 8-16
- Add crb script

* Mon Mar 14 2022 Troy Dawson <tdawson@redhat.com> - 8-15
- Remove the use of $releasever ( rhbz#1969500 )

* Fri Jan 28 2022 Troy Dawson <tdawson@redhat.com> - 8-14
- Remove epel8-playground repo
- Update playground section in README-epel-8-packaging.md

* Fri Sep 03 2021 Mohan Boddu <mboddu@bhujji.com> - 8-13
- Change the baseurl to point to source/tree for srpms

* Fri Jul 30 2021 Kevin Fenzi <kevin@scrye.com> - 8-12
- Enable certbot-renew.timer ( rhbz#1986205 )

* Thu Jun 03 2021 Carl George <carl@george.computer> - 8-11
- Add epel-next-release subpackage

* Sat Dec 05 2020 Kevin Fenzi <kevin@scrye.com> - 8-10
- Add x509watch.timer enabled by default. Fixes bug #1901721

* Sat Oct 31 2020 Kevin Fenzi <kevin@scrye.com> - 8-9
- Add countme feature for epel. Fixes bug #1825984

* Fri Dec 13 2019 Merlin Mathesius <mmathesi@redhat.com> - 8-8%{dist}
- Add modular repos.

* Thu Oct 10 2019 Stephen Smoogen <smooge@fedoraproject.org> - 8-7%{dist}
- Remove failovermethod from EPEL8 tree. It is no longer needed.

* Mon Sep 16 2019 Stephen Smoogen <smooge@fedoraproject.org> - 8-6%{dist}
- Change gpg key to use -8 versus -$releasever. This fixes bash problem

* Tue Aug  6 2019 Stephen Smoogen <smooge@fedoraproject.org> - 8-5%{dist}
- Fix playground release to have os/ on its name [Kevin Fenzi]
- Make sure all values of $release are $releasever


* Thu Aug  1 2019 Pablo Greco <pgreco@centosproject.org> - 8-4
- Use the correct var for dnf to expand
- Update playground source url
- Remove epel-modules repo
- Use https in baseurl

* Thu Aug  1 2019 Stephen Smoogen <smooge@fedoraproject.org> - 8-3
- Make sure that the key name is named correctly

* Thu Aug  1 2019 Stephen Smoogen <smooge@fedoraproject.org> - 8-2
- Make baseurl paths match dl.fedoraproject.org
- Add draft of epel8 packaging
- Fix docs

* Thu Jul 18 2019 Stephen Smoogen <smooge@smoogen-laptop.localdomain> - 8-1
- Update for RHEL-8
- Add playground repo data
- Clean out 90-epel.preset to make sure we dont override RHEL-8 items. Just add items in which EPEL needs.

* Mon Oct 02 2017 Kevin Fenzi <kevin@scrye.com> - 7-11
- Add Conflicts on fedora-release to prevent people from installing on Fedora systems. Fixes bug #1497702

* Sat Jun 24 2017 Kevin Fenzi <kevin@scrye.com> - 7-10
- Change mirrorlist= in repo files to be metalink= (as thats what they are). Fixes bug #1451212

* Tue Dec 27 2016 Kevin Fenzi <kevin@scrye.com> - 7-9
- Add preset for drbdlinks package. Fixes bug #1405744

* Sat Jul 23 2016 Kevin Fenzi <kevin@scrye.com> - 7-8
- Drop duplicate libstoragemgmt from presets. Fixes bug #1358971

* Fri Jun 03 2016 Kevin Fenzi <kevin@scrye.com> - 7-7
- Drop initial-setup from presets. Fixes bug #1342511

* Wed Mar 30 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 7-6
- Remove macros.epel; let epel-rpm-macros handle it instead.

* Tue Nov 25 2014 Rex Dieter <rdieter@fedoraproject.org> 7-5
- fix typo in macros.epel

* Fri Nov 21 2014 Rex Dieter <rdieter@fedoraproject.org> 7-4
- add systemd 90-epel.preset

* Fri Nov 21 2014 Rex Dieter <rdieter@fedoraproject.org> 7-3
- implement %%epel macro

* Tue Sep 02 2014 Kevin Fenzi <kevin@scrye.com> 7-2
- Make repo files config(noreplace). Fixes bug #1135576

* Thu Aug 28 2014 Dennis Gilmore <dennis@ausil.us> - 7-1
- enable gpg checking now we are out of beta

* Wed Jun 18 2014 Kevin Fenzi <kevin@scrye.com> 7-0.2
- Drop unneeded up2date post/postun
- Fixed up description.
- Fixes bugs #1052434 and #1093918

* Mon Dec 16 2013 Dennis Gilmore <dennis@ausil.us> - 7-0.1
- initial epel 7 build. gpg cheking is disabled

