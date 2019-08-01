# EPEL-8 Packaging Procedures

## Introduction

When a new Red Hat Enterprise Linux occurs, one of the steps to get
EPEL going for it is branching of various packages into new
namespace. The EPEL Steering Committee does not mass branch all
existing packages into the namespace because it has caused multiple
problems:

1. The package maintainers did not want to support the package in the
newer version of EPEL. Package maintainers may only want to support
certain versions of Enterprise Linux or may want to wait until their
favourite derivative appears.

2. The package does not work in the latest version of RHEL. With
multiple years between releases, software which worked on Fedora 18
which would branch to EPEL-7 may not exist anymore with Fedora 28 and
EPEL-8 would need a completely different version.

## Consumer request for packages

People who are interested in getting packages into EPEL should contact
the package maintainer through
[bugzilla](https://bugzilla.redhat.com/). This allows for the requests
to be tracked and if the primary maintainer is not interested in
branching to EPEL, other ones can step in and do so.

## EPEL Playground

We have added an additional set of channels for EPEL-8 called
playground. It is meant to be sort of like Fedora Rawhide so that
packagers can work on versions of software which are too fast moving
or will have large API changes from what they are putting in the
regular channel.

To try and make this transparent, we have made it so when a package is
built in epel8 it will normally also be built in
epel8-playground. This is done via a packages.cfg file which lists the
targets for fedpkg to build against. A successful package build will
then go through 2 different paths:

* epel8 package will go into bodhi to be put into epel8-testing
* epel8-playground will bypass bodhi and go directly into
  epel8-playground the next compose.

If a packager needs to focus only on epel8 or epel8-playground they
can edit packages.cfg to change the ```target= epel8
epel8-playground``` to ```target= epel8 ```.

Packages in epel8-playground are primarily to be used in the following
manner:

* To test out some new version of the package that might not be stable
  yet.

* To test out some new packaging of the package

* To test a major version change of the package that they want to land
  at the next epel8 minor release.

* To build a package that will never be stable enough for epel8, but
  still could be useful to some.

* At minor RHEL releases (ie, 8.1, 8.2) people can pull in big changes
  from playground to the main epel8 packages. Since people will be
  upgrading and paying more attention than usual anyhow at those
  points, it’s a great chance to do that change, but also you want to
  make sure it’s panned out, so you can test before hand in
  playground.

Consumers should be aware that packages in EPEL8-playground are there
without any Service Level Expectations. You may want to only cherry
pick packages from there as needed.

## Developer request for branching multiple packages

Branching is handled the same way as requesting a branch using `fedpkg
request-branch`. A maintainer can request an epel8 branch using
`fedpkg request-branch epel8` which will create a ticket in
https://pagure.io/releng/fedora-scm-requests/issues and Release
Engineering will process these requests.

To branch multiple packages please use this or a variant of this
script:

```
#!/usr/bin/sh
# Reminder to get an updated pagure token for releng tickets
# Usage: epel-8.sh foo bar goo blah blech
if [ $# -lt 1 ]
then
    echo "At least one package name should be provided"
else
    TMPDIR=`mktemp -d /tmp/epel8.XXXXXX`
    pushd "$TMPDIR"
    for pkg in "$@"
    do
        fedpkg clone "$pkg"
        pushd "$pkg"
        fedpkg request-branch epel8
	    fedpkg request-branch epel8-playground
        popd
    done
    rm -rfv "$TMPDIR"
fi
```

Releng will then work through the tickets in the system which is
adding branches to the PDC and src.fedoraproject.org.


## Known Issues

1. /usr/bin/python does not exist. Choose ``/usr/bin/python3`` or
``/usr/bin/python2`` and patch appropriately.

2. ``python2-sphinx`` is not shipped. Most packages should work with
python3-sphinx, and if it doesn't please open a bug. The python team
has been good about making fixes for this.

3. When branching python packages, be aware that python in EL-8 is
python36 and not the version currently in rawhide. This has come up
with a couple of test packages where they assumed python37 or later.

4. ``systemd-rpm-macros`` is not a separate packages. If needed, used
``BuildRequires: systemd``

5. While EL-8 comes with platform-python, it should NOT be used in
``Requires:`` unless absolutely neccessary. python3 should be used
instead. (Exceptions can be made but will be rare and need
justification.)

**Accepted Exceptions:**
* Use python3.6dist(coverage) instead of python3-coverage. This
  package is not shipped but is needed in %check code.

6. Sometimes RHEL8 only has a python3 package for a dependency you
need for your build. (Example: python-bleach requires
python2-html5lib, but RHEL8 provides only python3-html5lib). For
EPEL-8.0 we only suggest one choice:

* Choose not to have the python2 part of your package and patch
  whatever to use python3.

7. Python2 packages are discouraged. RHEL-8 will contain python2.7
until probably the end of life of RHEL-7. However support upstream
will only be minimal. When modularity occurs, we suggest that you make
whatever python2 packages modules which can be pulled out when
RHEL-8.N no longer has python2.

8. While a RHEL src.rpm might produce a -devel package, it may not
currently be in the build repository. When running into this please
open a ticket with https://pagure.io/epel/new_issue for us to put in a
request for it to be added to Red Hat's Code Ready Builder. After
modularity is enabled, changes to what is done will be needed.

9. EPEL-8.0 may not work with the RHEL-8.1 beta. There seem to be
changes in dnf and zchunk which we have not worked out. This line will
be updated.


## Definitions

1. Package maintainer. Person who has accepted responsibility to
package and maintain software in the Fedora Project ecosystem. The
main packager is usually someone focused on Fedora Linux, and
secondary packagers may be focused on particular use cases like EPEL.

2. Consumer. A person who has subscribed to EPEL for packages but is
not a maintainer.

3. PDC. Product Definition Center. A tool to help list the lifetime
and permissions that a product has so that branching and updates can
be better managed.
