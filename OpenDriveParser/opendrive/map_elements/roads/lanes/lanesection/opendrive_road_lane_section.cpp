#include "opendrive_road_lane_section.hpp"

OpenDriveRoadLaneSection::OpenDriveRoadLaneSection()
{
   center_lanes_ = new std::vector<OpenDriveRoadLane*>();
   left_lanes_ = new std::vector<OpenDriveRoadLane*>();
   right_lanes_ = new std::vector<OpenDriveRoadLane*>();
}

OpenDriveRoadLaneSection::~OpenDriveRoadLaneSection()
{
    for(size_t i=0; i<center_lanes_->size();++i) delete (*center_lanes_)[i];
    delete center_lanes_;
    for(size_t i=0; i<left_lanes_->size();++i) delete (*left_lanes_)[i];
    delete left_lanes_;
    for(size_t i=0; i<right_lanes_->size();++i) delete (*right_lanes_)[i];
    delete right_lanes_;
}

