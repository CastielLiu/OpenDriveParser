#ifndef OPENDRIVEROADLANE_HPP
#define OPENDRIVEROADLANE_HPP

// Project includes
#include "opendrive/map_elements/opendrive_map_element.hpp"
#include "opendrive/map_elements/roads/lanes/lane/link/opendriveroad_lane_link.hpp"


class OpenDriveRoadLanePoint : public OpenDriveMapElement
{
public:
    OpenDriveRoadLanePoint();
    double x_,y_,z_;
    std::map<QString, std::function<bool(QString)>> function_map_ = {
      {"x", std::bind(&OpenDriveParseUtil::set_parsed_value<double>,
                       std::placeholders::_1, std::ref(x_))},
      {"y", std::bind(&OpenDriveParseUtil::set_parsed_value<double>,
                       std::placeholders::_1, std::ref(y_))},
      {"z", std::bind(&OpenDriveParseUtil::set_parsed_value<double>,
                     std::placeholders::_1, std::ref(z_))}
    };
};

class OpenDriveRoadLane : public OpenDriveMapElement
{
 public:
  OpenDriveRoadLane();
  ~OpenDriveRoadLane();
  int get_id()
  {
      return id_;
  }
  QString get_turn_type()
  {
      return turn_type_;
  }
  QString get_type()
  {
      return type_;
  }

  OpenDriveRoadLaneLink* link_;
  std::vector<OpenDriveRoadLanePoint *> points;

  std::map<QString, std::function<bool(QString)>> function_map_ = {
    {"id", std::bind(&OpenDriveParseUtil::set_parsed_value<int>,
                     std::placeholders::_1, std::ref(id_))},
    {"turnType", std::bind(&OpenDriveParseUtil::set_parsed_value<QString>,
                     std::placeholders::_1, std::ref(turn_type_))},
    {"type", std::bind(&OpenDriveParseUtil::set_parsed_value<QString>,
                   std::placeholders::_1, std::ref(type_))}
  };

private:
  int id_;
  QString turn_type_;
  QString type_;
};

#endif // OPENDRIVEROADLANE_HPP
