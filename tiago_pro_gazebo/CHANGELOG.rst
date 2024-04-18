^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package tiago_pro_gazebo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.0.5 (2024-04-18)
------------------
* Merge branch 'omm/feat/public_sim_check' into 'humble-devel'
  is_public_sim launch support
  See merge request robots/tiago_pro_simulation!18
* is_public_sim launch support
* Merge branch 'omm/feat/tuck_arm' into 'humble-devel'
  Added tuck arm script
  See merge request robots/tiago_pro_simulation!17
* Added tuck arm script
* Merge branch 'fix/renamed-params' into 'humble-devel'
  removed laser pipeline
  See merge request robots/tiago_pro_simulation!16
* removed laser pipeline
* Merge branch 'dtk/feat/public_sim_check' into 'humble-devel'
  Show error when public sim is used without the is_public_sim arg set to true
  See merge request robots/tiago_pro_simulation!15
* Show error when public sim is used without the is_public_sim arg set to true
* Contributors: David ter Kuile, Oscar, andreacapodacqua, davidterkuile

1.0.4 (2024-03-27)
------------------
* Merge branch 'dtk/fix/missing-nav-dependency' into 'humble-devel'
  Add missing 2dnav dependency
  See merge request robots/tiago_pro_simulation!14
* Add missing 2dnav dependency
* Contributors: davidterkuile

1.0.3 (2024-03-26)
------------------
* Merge branch 'feat/ros2-navigation' into 'humble-devel'
  Feat/ros2 navigation
  See merge request robots/tiago_pro_simulation!13
* linters
* using robot_name
* private simulation for navigation and mapping
* Contributors: andreacapodacqua

1.0.2 (2024-03-22)
------------------
* Merge branch 'dtk/fix/add-movit-config' into 'humble-devel'
  Add dependency tiago-pro-moveit-config
  See merge request robots/tiago_pro_simulation!12
* Add dependency tiago-pro-moveit-config
* Contributors: Noel Jimenez, davidterkuile

1.0.1 (2024-03-22)
------------------
* Merge branch 'dtk/fix/restructure' into 'humble-devel'
  restructure launch files
  See merge request robots/tiago_pro_simulation!10
* Change to double quotes
* Update copyright year
* Change common param to is_public_sim
* restructure launch files
* Merge branch 'dtk/fix/add-linter-tests' into 'humble-devel'
  Dtk/fix/add linter tests
  See merge request robots/tiago_pro_simulation!9
* Fix linter formatting issues
* Add tests packages to package.xml
* Add linter testing
* Merge branch 'feat/launch_moveit_by_default' into 'humble-devel'
  Launch MoveIt 2 by default
  See merge request robots/tiago_pro_simulation!8
* Launch MoveIt 2 by default
* Contributors: David ter Kuile, Jordan Palacios, Noel Jimenez, davidterkuile

1.0.0 (2024-01-30)
------------------
* Merge branch 'ros2-migration' into 'humble-devel'
  Ros2 migration
  See merge request robots/tiago_pro_simulation!5
* add the world_name param
* remove pal_hardware_gazebo depend
* update to 3.8 the cmake_minimum_required Version
* update launch files
* integration launch file for simulation
* delete find_package(catkin REQUIRED)
* migration to ROS2 CMakeLists and package.xml
* Merge branch 'change_name' into 'master'
  Change tiago_v2_prototype to tiago_pro
  See merge request robots/tiago_pro_simulation!3
* Change tiago_v2_prototype to tiago_pro
* Contributors: Adria Roig, Jordan Palacios, ileniaperrella, thomaspeyrucain
