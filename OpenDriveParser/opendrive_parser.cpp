// Qt includes
#include <QDebug>
#include <QXmlInputSource>
#include <QXmlSimpleReader>

// Project includes
#include "opendrive_parser.hpp"
#include "ui_opendrive_parser.h"

OpenDriveParser::OpenDriveParser(QWidget *parent) :
  QMainWindow(parent), ui(new Ui::OpenDriveParser) {
  ui->setupUi(this);
}

OpenDriveParser::OpenDriveParser(QString od_map, QWidget *parent) :
  QMainWindow(parent), ui(new Ui::OpenDriveParser) {
  ui->setupUi(this);

  opendrive_map_file_ = new QFile(od_map);
}

OpenDriveParser::~OpenDriveParser()
{
  if (opendrive_map_file_)
      delete opendrive_map_file_;
  if(parse_handler_)
      delete parse_handler_;
  delete ui;
}

void OpenDriveParser::set_map_file(QString map_file) {
  if (opendrive_map_file_) delete opendrive_map_file_;
  opendrive_map_file_ = new QFile(map_file);
}

bool OpenDriveParser::parse_map_file(OpenDriveMap* map) {
  QXmlSimpleReader xml_reader;
  QXmlInputSource* input_source = new QXmlInputSource(opendrive_map_file_);
  parse_handler_ = new OpenDriveParseHandler(map);
  xml_reader.setContentHandler(parse_handler_);
  xml_reader.setErrorHandler(parse_handler_);

  bool parse_ok = xml_reader.parse(input_source);

  if (!parse_ok)
      qDebug() << "[PARSER] Parse failed!";
  else
      qDebug() << "[PARSER] Parse succeeded!";

  delete input_source;
  return parse_ok;
}

bool OpenDriveParser::save_road_points(const QString& path)
{
    if(!parse_handler_)
    {
        qDebug() << "please excute parse_map_file() first!!!";
        return false;
    }
    return parse_handler_->save_road_points(path);
}

