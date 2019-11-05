#include "opendrive_road_lane.hpp"

OpenDriveRoadLanePoint::OpenDriveRoadLanePoint() : OpenDriveMapElement() {}

OpenDriveRoadLane::OpenDriveRoadLane() : OpenDriveMapElement() { }


OpenDriveRoadLane::~OpenDriveRoadLane()
{
    for(size_t i=0; i<points.size();++i)
        delete points[i];
}
