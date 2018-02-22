# Adapted from
# https://build.opensuse.org/package/view_file/home:bruno_friedmann:branches:Application:Geo/cloudcompare/cloudcompare.spec
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2016 Ioda-Net Sàrl, Charmoille, Switzerland. Bruno Friedmann
# Copyright (c) 2017 Miro Hrončok and possibly others
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.


%global edition Release
%global cname   CloudCompare
Name:           cloudcompare
Version:        2.9.1
Release:        1%{?dist}
Summary:        3D point cloud and mesh processing software

# Main part is GPLv2+
# CCLib is LGPLv2+
# Plugins from Source1 and Source2 are MIT
# dxflib is GPLv2+
# shapelib is (LGPLv2+ or MIT)
# as the result is compiled into one piece, it should be:
License:        GPLv2+

URL:            http://www.cloudcompare.org/

Source0:        https://github.com/%{cname}/%{cname}/archive/v%{version}/%{cname}-%{version}.tar.gz

# git submodules
%global pr_commit f42872b45ac35bf85efc662d348bb5d8ac9e5577
Source1:        https://github.com/%{cname}/PoissonRecon/archive/%{pr_commit}/PoissonRecon-%{pr_commit}.tar.gz

%global nh_commit 61ba8056d72eedffadb838d9051cc8975ec7a825
Source2:        https://github.com/%{cname}/normals_Hough/archive/%{nh_commit}/normals_Hough-%{nh_commit}.tar.gz

# desktop files
Source3:        %{name}.desktop
Source4:        ccviewer.desktop

BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
BuildRequires:  cmake >= 3
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  laszip-devel
BuildRequires:  libgomp
BuildRequires:  liblas-devel
BuildRequires:  pkgconfig(gdal)
BuildRequires:  pkgconfig(cunit)
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(eigen3)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(pkg-config)
BuildRequires:  pkgconfig(shapelib)
BuildRequires:  pkgconfig(Qt3Support)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Designer)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Help)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5OpenGL)
BuildRequires:  pkgconfig(Qt5OpenGLExtensions)
BuildRequires:  pkgconfig(Qt5PrintSupport)
BuildRequires:  pkgconfig(Qt5Script)
BuildRequires:  pkgconfig(Qt5ScriptTools)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  pkgconfig(Qt5UiTools)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(Qt5XmlPatterns)
BuildRequires:  pkgconfig(xerces-c)
BuildRequires:  pkgconfig(zlib)

Provides:       bundled(dxflib) = 3.3.4
Provides:       %{cname} = %{version}-%{release}
%{?_isa:Provides:       %{cname}%{_isa} = %{version}-%{release}}

Requires:       hicolor-icon-theme

# Do not RPM provide .so files only used internally:
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$
%global __requires_exclude ^lib(Q)?CC_.*$

%description
CloudCompare is a 3D point cloud (and triangular mesh) processing software.
It has been originally designed to perform comparison between two 3D points
clouds (such as the ones obtained with a laser scanner) or between a point
cloud and a triangular mesh.
It relies on a specific octree structure that enables great performances in
this particular function. It was also meant to deal with huge point clouds
(typically more than 10 millions points, and up to 120 millions with 2 Gb of
memory).

Afterwards, it has been extended to a more generic point cloud processing
software, including many advanced algorithms (registration, resampling,
color/normal/scalar fields handling, statistics computation, sensor
management, interactive or automatic segmentation, display enhancement...).

%prep
%autosetup -n %{cname}-%{version} -p1

rmdir plugins/qPoissonRecon/PoissonReconLib
tar -xf %{SOURCE1}
mv PoissonRecon-%{pr_commit} plugins/qPoissonRecon/PoissonReconLib

rmdir plugins/qHoughNormals/normals_Hough
tar -xf %{SOURCE2}
mv normals_Hough-%{nh_commit} plugins/qHoughNormals/normals_Hough

# On 64bits, change /usr/lib/cloudcompare to /usr/lib64/cloudcompare
sed -i 's|lib/%{name}|%{_lib}/%{name}|g' $(grep -r lib/%{name} -l)

# Remove french TeX docs
rm -rf doc/fr*

# Remove bundle shapelib https://github.com/CloudCompare/CloudCompare/issues/497
rm -rf contrib/shapelib-*
sed -i 's/add_subdirectory.*//' contrib/ShapeLibSupport.cmake
sed -i 's/ SHAPELIB / shp /g' plugins/qFacets/CMakeLists.txt contrib/ShapeLibSupport.cmake

%build
mkdir build
pushd build

%cmake \
   -DCMAKE_BUILD_TYPE=%{edition} \
   -DCMAKE_INSTALL_RPATH=%{_libdir}/%{name} \
   -DEIGEN_ROOT_DIR=%{_includedir}/eigen3 \
   -DGDAL_LIB_SRC_DIR=%{_includedir} \
   -DINSTALL_QANIMATION_PLUGIN=ON \
   -DINSTALL_QBLUR_PLUGIN=ON \
   -DINSTALL_QBROOM_PLUGIN=ON \
   -DINSTALL_QCSF_PLUGIN=ON \
   -DINSTALL_QDUMMY_PLUGIN=OFF \
   -DINSTALL_QEDL_PLUGIN=ON \
   -DINSTALL_QFACETS_PLUGIN=ON \
   -DINSTALL_QHOUGH_NORMALS_PLUGIN=ON \
   -DINSTALL_QHPR_PLUGIN=ON \
   -DINSTALL_QKINECT_PLUGIN=OFF \
   -DINSTALL_QM3C2_PLUGIN=ON \
   -DINSTALL_QPCL_PLUGIN=OFF \
   -DINSTALL_QPCV_PLUGIN=ON \
   -DINSTALL_QPHOTOSCAN_IO_PLUGIN=ON \
   -DINSTALL_QPOISSON_RECON_PLUGIN=ON \
   -DINSTALL_QRANSAC_SD_PLUGIN=ON \
   -DINSTALL_QSRA_PLUGIN=ON \
   -DINSTALL_QSSAO_PLUGIN=ON \
   -DLIBLAS_INCLUDE_DIR=%{_includedir}/liblas \
   -DLIBLAS_RELEASE_LIBRARY_FILE=%{_libdir}/liblas.so.3 \
   -DOPTION_SUPPORT_3DCONNEXION_DEV=OFF \
   -DOPTION_USE_DXF_LIB=ON \
   -DOPTION_USE_GDAL=ON \
   -DOPTION_USE_LIBLAS=ON \
   -DOPTION_USE_SHAPE_LIB=ON \
   -DSHAPELIB_SOURCE_DIR=%{_includedir} \
   ..

#   -DINSTALL_QGMMREG_PLUGIN=ON \ # Fails with our vxl


%make_build VERBOSE=1
popd

%install
pushd build
%make_install VERBOSE=1
popd

# lower-case symblinks
ln -s ./%{cname} %{buildroot}%{_bindir}/%{name}
ln -s ./ccViewer %{buildroot}%{_bindir}/ccviewer

# icons
for RES in 16 32 64 256; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${RES}x${RES}/apps/
  cp qCC/images/icon/cc_icon_${RES}.png %{buildroot}%{_datadir}/icons/hicolor/${RES}x${RES}/apps/%{name}.png
  cp qCC/images/icon/cc_viewer_icon_${RES}.png %{buildroot}%{_datadir}/icons/hicolor/${RES}x${RES}/apps/ccviewer.png
done

# desktop files
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE3}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE4}


%files
%doc README.md CONTRIBUTING.md CHANGELOG.md doc
%license license.txt license_headers.txt
%{_bindir}/%{name}
%{_bindir}/%{cname}
%{_bindir}/ccviewer
%{_bindir}/ccViewer
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%exclude %{_datadir}/%{name}/CHANGELOG.md
%exclude %{_datadir}/%{name}/license.txt
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/applications/*.desktop

%changelog
* Thu Feb 22 2018 Miro Hrončok <mhroncok@redhat.com> - 2.9.1-1
- Updated to 2.9.1
- Remove merged patch
- Removed obsolete icon scriptlets
- Require hicolor-icon-theme
- Use make macros

* Sat Sep 09 2017 Miro Hrončok <mhroncok@redhat.com> - 2.8.1-1
- Updated to 2.8.1

* Mon Jan 16 2017 Miro Hrončok <mhroncok@redhat.com> - 2.8.0-1
- Initial package adapted from openSUSE package
