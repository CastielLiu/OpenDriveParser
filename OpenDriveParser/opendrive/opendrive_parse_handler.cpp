// Qt includes
#include <QDebug>
#include <QString>

// C++ includes
#include <typeinfo>  // typeid operator

// Project includes
#include "opendrive_parse_handler.hpp"
#include "opendrive/opendrive_map.hpp"
#include "opendrive/map_elements/opendrive_map_element.hpp"
#include "opendrive/map_elements/roads/opendrive_road.hpp"
#include "opendrive/map_elements/roads/lanes/lane/opendrive_road_lane.hpp"
#include "opendrive/map_elements/roads/lanes/lane/link/opendrive_road_lane_link_predecessor.hpp"

OpenDriveParseHandler::OpenDriveParseHandler(OpenDriveMap* map) :
  map_(map)
{
    out_file_.open("/home/wendao/Desktop/map.txt");
}

OpenDriveParseHandler::~OpenDriveParseHandler()
{
    if(out_file_.is_open())
    {
        out_file_.close();
    }
}

bool OpenDriveParseHandler::startElement(const QString& namespaceURI,
                                         const QString& localName,
                                         const QString& qName,
                                         const QXmlAttributes& atts) {
  Q_UNUSED(localName);
  Q_UNUSED(namespaceURI);

//  qDebug() << "Element name:" << qName;
//  for (int i = 0; i < atts.length(); i++)
//  {
//      qDebug() << "  attribute" << atts.qName(i) << "has value" << atts.value(i);
//  }

  if (qName == "header")
  {
    map_->header_ = new OpenDriveMapHeader();
    set_map_elements(atts, map_->header_->function_map_);

  }
  else if (qName == "road")
  {
    map_->roads_.push_back(new OpenDriveRoad());
    last_link_parent_.push(map_->roads_.back());
    set_map_elements(atts, map_->roads_.back()->function_map_);
  }
  else if (qName == "link")
  {
    if (!last_link_parent_.size()) {
      qDebug() << "OpenDriveParseUtil: Found a link element with no valid "
                  "parent element!";
      return false;
    }

    OpenDriveMapElement* link_parent = last_link_parent_.top();
//  qDebug()<< "typeid(*link_parent).name()" << typeid(*link_parent).name();
    if (typeid(*link_parent).hash_code() == typeid(OpenDriveRoad).hash_code())
    {
      OpenDriveRoadLink* new_link = new OpenDriveRoadLink();
      static_cast<OpenDriveRoad*>(link_parent)->link_ = new_link;
      last_link_.push(new_link);
    }
    else if (typeid(*link_parent).hash_code() == typeid(OpenDriveRoadLane).hash_code())
    {
      OpenDriveRoadLaneLink* new_link = new OpenDriveRoadLaneLink();
      static_cast<OpenDriveRoadLane*>(link_parent)->link_ = new_link;
      last_link_.push(new_link);
    }

  }
  else if (qName == "predecessor")
  {
    OpenDriveMapElement* last_link = last_link_.top();

    if (typeid(*last_link).hash_code() == typeid(OpenDriveRoadLink).hash_code())
    {
      OpenDriveRoadLinkPredecessor* predecessor = new OpenDriveRoadLinkPredecessor();

      set_map_elements(atts, predecessor->function_map_);
      static_cast<OpenDriveRoadLink*>(last_link)->predecessor_ = predecessor;
    }
    else if (typeid(*last_link).hash_code() == typeid(OpenDriveRoadLaneLink).hash_code())
    {
      OpenDriveRoadLaneLinkPredecessor* predecessor = new OpenDriveRoadLaneLinkPredecessor();
      set_map_elements(atts, predecessor->function_map_);
      static_cast<OpenDriveRoadLaneLink*>(last_link)->predecessor_ = predecessor;
    }
  }
  else if (qName == "lanes")
  {
    map_->roads_.back()->lanes_ = new OpenDriveRoadLanes();
  }
  else if (qName == "laneSection")
  {
    OpenDriveRoadLaneSection* lane_section = new OpenDriveRoadLaneSection();
    set_map_elements(atts, lane_section->function_map_);
    map_->roads_.back()->lanes_->lane_sections_.push_back(lane_section);
    last_lane_section_parent_.push(map_->roads_.back()->lanes_->lane_sections_.back());
  }
  else if (qName == "laneOffset")
  {
    OpenDriveRoadLaneOffset* lane_offset = new OpenDriveRoadLaneOffset();
    set_map_elements(atts, lane_offset->function_map_);
    map_->roads_.back()->lanes_->lane_offsets_.push_back(lane_offset);
  }
  else if(qName == "left")
      last_dir_lanes_parent_.push(last_lane_section_parent_.top()->left_lanes_);
  else if(qName == "center")
      last_dir_lanes_parent_.push(last_lane_section_parent_.top()->center_lanes_);
  else if(qName == "right")
      last_dir_lanes_parent_.push(last_lane_section_parent_.top()->right_lanes_);
  else if(qName == "lane")
  {
      OpenDriveRoadLane * lane = new OpenDriveRoadLane();
      set_map_elements(atts,lane->function_map_);
      last_dir_lanes_parent_.top()->push_back(lane);
      last_points_parent_.push(lane);
      last_link_parent_.push(lane);
  }
  else if(qName == "point")
  {
      OpenDriveRoadLanePoint *point = new OpenDriveRoadLanePoint();
      set_map_elements(atts, point->function_map_);

      qDebug() <<"+++++++++++++++++++" << point->x_ << "\t" << point->y_ << "\t" << point->z_ ;

      if(last_points_parent_.size())
      {
          OpenDriveRoadLane *last_lane = static_cast<OpenDriveRoadLane *>(last_points_parent_.top());
          last_lane->points.push_back(point);
          //if(last_lane->get_id()==0)
              out_file_ << point->x_ << "\t" << point->y_ << "\t" << point->z_ << std::endl;
      }
  }
  else
  {
    ;
  }

  return true;
}

bool OpenDriveParseHandler::endElement(const QString& namespaceURI,
                                       const QString& localName,
                                       const QString& qName) {
  Q_UNUSED(namespaceURI);
  Q_UNUSED(localName);
  if (qName == "road")
    last_link_parent_.pop();
  else if (qName == "link")
  {
    last_link_.pop();
  }
  else if (qName == "laneSection")
      last_lane_section_parent_.pop();
  else if(qName == "left" || qName == "center" || qName == "right")
      last_dir_lanes_parent_.pop();
  else if(qName == "lane")
  {
      last_link_parent_.pop();
      last_points_parent_.pop();
  }
  else if (qName == "type")
  {
      ;
  }
  else if (qName == "object"    || qName == "objectReferece" ||
             qName == "tunnel"    || qName == "bridge"         ||
             qName == "signal"    || qName == "signalReference")
  {
    last_validity_parent_.pop();
  }

  return true;
}

bool OpenDriveParseHandler::set_map_elements(const QXmlAttributes& atts,
        const std::map<QString, std::function<bool (QString)>>& function_map_) {
  bool success = true;

  for (int i = 0; i < atts.count(); i++) {
    auto map_element = function_map_.find(atts.qName(i));

    if (map_element != function_map_.end()) {
      map_element->second(atts.value(i));
    } else {
      success = false;
    }
  }

  return success;
}

OpenDriveRoad* OpenDriveParseHandler::get_last_added_road() {
  OpenDriveRoad* last_road = nullptr;

  if (map_) {
    if (map_->roads_.size()) {
        last_road = map_->roads_[map_->roads_.size() - 1];
    }
  }

  return last_road;
}

bool OpenDriveParseHandler::save_road_points(const QString& path)
{
    QDir dir(path);
    if(!dir.exists())
    {
        if(!dir.mkdir(path))
        {
            qDebug() << "create directory " << path << "failed!!";
            return false;
        }
    }

    for(size_t i=0; i<map_->roads_.size(); ++i)
    {
        auto &road = map_->roads_[i];
        QString roadName = road->get_name();
        //QString fileName = path + "/" + roadName + ".txt";
        QString fileName = path + "/" + QString::number(i) + ".txt";
        std::ofstream out_file;
        out_file.open(fileName.toStdString());
        if(!out_file.is_open())
        {
            std::cout << "open " << fileName.toStdString() << "failed !!!" << std::endl;
            return false;
        }
        auto &laneSections = road->lanes_->lane_sections_;
        for(size_t j=0; j<laneSections.size();++j)
        {
            auto &centerLanes = laneSections[j]->center_lanes_;
            for(size_t k=0; k<centerLanes->at(0)->points.size(); ++k)
            {
                auto point = centerLanes->at(0)->points[k];
                out_file << point->x_ << "\t" << point->y_ << "\t" << point->z_ << std::endl;
            }
        }

    }

    return true;
}
