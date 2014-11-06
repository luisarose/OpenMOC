#include "Cell.h"


int Cell::_n = 0;

static int auto_id = 10000;


/**
 * @brief Returns an auto-generated unique Cell ID.
 * @details This method is intended as a utility method for users writing
 *          OpenMOC input files. The method makes use of a static Cell
 *          ID which is incremented each time the method is called to enable
 *          unique generation of monotonically increasing IDs. The method's
 *          first ID begins at 10000. Hence, user-defined Cell IDs greater
 *          than or equal to 10000 are prohibited.
 */
int cell_id() {
  int id = auto_id;
  auto_id++;
  return id;
}


/**
 * @brief Default constructor used in rings/sectors subdivision of Cells.
 */
Cell::Cell() {
}


/**
 * @brief Constructor sets the unique and user-specifed IDs for this Cell.
 * @param id the user-specified Cell ID
 * @param universe the ID of the Universe within which this Cell resides
 */
Cell::Cell(int universe, int id) {

  /* If the user did not define an optional ID, create one */
  if (id == 0)
    _id = cell_id();

  /* If the user-defined ID is in the prohibited range, return an error */
  else if (id >= 10000)
    log_printf(ERROR, "Unable to set the ID of a cell to %d since cell IDs "
               "greater than or equal to 10000 is probibited by OpenMOC.", id);

  /* Use the user-defined ID */
  else
    _id = id;

  _uid = _n;
  _n++;
  _universe = universe;
}


/**
 * @brief Destructor clears vector of Surface pointers bounding the Cell.
 */
Cell::~Cell() {
  _surfaces.clear();
}


/**
 * @brief Return the Cell's unique ID.
 * @return the Cell's unique ID
 */
int Cell::getUid() const {
  return _uid;
}


/**
 * @brief Return the Cell's user-specified ID.
 * @return the Cell's user-specified ID
 */
int Cell::getId() const {
  return _id;
}


/**
 * @brief Return the Cell type (FILL or MATERIAL).
 * @return the Cell type
 */
cellType Cell::getType() const {
  return _cell_type;
}


/**
 * @brief Return the ID of the Universe within which this Cell resides.
 * @return the Universe ID
 */
int Cell::getUniverseId() const {
  return _universe;
}


/**
 * @brief Return the number of Surfaces in the Cell.
 * @return the number of Surfaces
 */
int Cell::getNumSurfaces() const {
  return _surfaces.size();
}


/**
 * @brief Return the std::map of Surface pointers and halfspaces (+/-1) for all
 *        surfaces bounding the Cell.
 * @return std::map of Surface pointers and halfspaces
 */
std::map<int, surface_halfspace> Cell::getSurfaces() const {
  return _surfaces;
}


/**
 * @brief Set the ID for the Universe within which this Cell resides.
 * @param universe the Universe's user-specified ID
 */
void Cell::setUniverse(int universe) {
  _universe = universe;
}


/**
 * @brief Insert a Surface into this Cells container.
 * @param halfspace the Surface halfspace (+/-1)
 * @param surface a pointer to the Surface
 */
void Cell::addSurface(int halfspace, Surface* surface) {

  if (halfspace != -1 && halfspace != +1)
    log_printf(ERROR, "Unable to add surface %d to cell %d since the halfspace"
               " %d is not -1 or 1", surface->getId(), _id, halfspace);

  surface_halfspace* new_surf_half = new surface_halfspace;
  new_surf_half->_surface = surface;
  new_surf_half->_halfspace = halfspace;
  _surfaces[surface->getId()] = *new_surf_half;
}


/**
 * @brief Determines whether a Point is contained inside a Cell.
 * @details Queries each Surface inside the Cell to determine if the Point
 *          is on the same side of the Surface. This point is only inside
 *          the Cell if it is on the same side of every Surface in the Cell.
 * @param point a pointer to a Point
 */
bool Cell::cellContainsPoint(Point* point) {

  /* Loop over all Surfaces inside the Cell */
  std::map<int, surface_halfspace>::iterator iter;
  for (iter = _surfaces.begin(); iter != _surfaces.end(); ++iter) {

    /* Return false if the Point is not in the correct Surface halfspace */
    if (iter->second._surface->evaluate(point) * iter->second._halfspace < -ON_SURFACE_THRESH)
      return false;
  }

  /* Return true if the Point is in the correct halfspace for each Surface */
  return true;
}


/**
 * @brief Determines whether a Point is contained inside a Cell.
 * @details Queries each Surface inside the Cell to determine if the Point
 *          is on the same side of the Surface. This Point is only inside
 *          the Cell if it is on the same side of every Surface in the Cell.
 * @param coords a pointer to a localcoord
 */
bool Cell::cellContainsCoords(LocalCoords* coords) {
  return cellContainsPoint(coords->getPoint());
}


/**
 * @brief Computes the minimum distance to a Surface from a Point with a given
 *        trajectory at a certain angle.
 * @details If the trajectory will not intersect any of the Surfaces in the
 *          Cell returns INFINITY.
 * @param point the Point of interest
 * @param angle the angle of the trajectory (in radians from \f$[0,2\pi]\f$)
 * @param min_intersection a pointer to the intersection Point that is found
 */
double Cell::minSurfaceDist(Point* point, double angle,
                            Point* min_intersection) {

  double min_dist = INFINITY;
  double d;
  Point intersection;

  std::map<int, surface_halfspace>::iterator iter;

  /* Loop over all of the Cell's Surfaces */
  for (iter = _surfaces.begin(); iter != _surfaces.end(); ++iter) {

    /* Find the minimum distance from this surface to this Point */
    d = iter->second._surface->getMinDistance(point, angle, &intersection);

    /* If the distance to Cell is less than current min distance, update */
    if (d < min_dist) {
      min_dist = d;
      min_intersection->setX(intersection.getX());
      min_intersection->setY(intersection.getY());
    }
  }

  return min_dist;
}


/**
 * Constructor sets the user-specified and unique IDs for this CellBasic.
 * @param universe the ID for the Universe within which this CellBasic resides
 * @param material the ID for the Material which fills this CellBasic
 * @param rings the number of equal volume rings to divide this Cell into
 *        (the default is zero)
 * @param sectors the number of angular sectors to divide this Cell into
 *        (the default is zero)
 * @param id the user-specified Cell ID
 */
CellBasic::CellBasic(int universe, int material, int rings,
                     int sectors, int id): Cell(universe, id) {

  _cell_type = MATERIAL;
  _material = material;
  setNumRings(rings);
  setNumSectors(sectors);
}



/**
 * @brief Return the ID of the Material filling the CellBasic.
 * @return the Material's ID
 */
int CellBasic::getMaterial() const {
  return _material;
}


/**
 * @brief Return the number of rings in the Cell.
 * @return the number of rings
 */
int CellBasic::getNumRings() {
  return _num_rings;
}


/**
 * @brief Return the number of sectors in the Cell.
 * @return the number of sectors
 */
int CellBasic::getNumSectors() {
  return _num_sectors;
}


/**
 * @brief Set the Cell's number of rings.
 * @param num_rings the number of rings in this Cell
 */
void CellBasic::setNumRings(int num_rings) {
  if (num_rings < 0)
    log_printf(ERROR, "Unable to give %d rings to Cell %d since this is "
               "a negative number", num_rings, _id);

  _num_rings = num_rings;
}


/**
 * @brief Set the Cell's number of sectors.
 * @param num_sectors the number of sectors in this Cell
 */
void CellBasic::setNumSectors(int num_sectors) {
  if (num_sectors < 0)
    log_printf(ERROR, "Unable to give %d sectors to Cell %d since this is "
               "a negative number", num_sectors, _id);

  /* By default, a ring is considered to have a single sector in [0, 2*pi] */
  if (num_sectors == 1)
    _num_sectors = 0;

  else
    _num_sectors = num_sectors;
}


/**
 * @brief Sets the ID for the Material filling this Cell.
 * @param material_id the new Material filling this Cell
 */
void CellBasic::setMaterial(int material_id) {
  _material = material_id;
}


/**
 * @brief Create a duplicate of the CellBasic.
 * @return a pointer to the clone
 */
CellBasic* CellBasic::clone() {

  /* Construct new Cell */
  CellBasic* new_cell = new CellBasic(_universe, _material,
                                      _num_rings, _num_sectors);

  /* Loop over all of this Cell's Surfaces and add them to the clone */
  std::map<int, surface_halfspace>::iterator iter;

  for (iter = _surfaces.begin(); iter != _surfaces.end(); ++iter)
    new_cell->addSurface(iter->second._halfspace, iter->second._surface);

  return new_cell;
}


/**
 * @brief Subdivides the Cell into clones for fuel pin angular sectors.
 */
void CellBasic::sectorize() {

  /* If the user didn't request any sectors, don't make any */
  if (_num_sectors == 0)
    return;

  double azim_angle;
  double delta_azim = 2. * M_PI / _num_sectors;
  double A, B;

  /* A container for each of the bouding planes for the sector Cells */
  std::vector<Plane*> planes;

  log_printf(DEBUG, "Sectorizing Cell %d with %d sectors",_id, _num_sectors);

  /* Create each of the bounding planes for the sector Cells */
  for (int i=0; i < _num_sectors; i++) {

    /* Figure out the angle for this plane */
    azim_angle = i * delta_azim;

    /* Instantiate the plane */
    A = cos(azim_angle);
    B = sin(azim_angle);
    Plane* plane = new Plane(A, B, 0.);
    planes.push_back(plane);

    log_printf(DEBUG, "Created sector Plane id = %d, angle = %f, A = %f, "
               "B = %f", i, azim_angle, A, B);
  }

  /* Create sectors using disjoint halfspaces of pairing Planes */
  for (int i=0; i < _num_sectors; i++) {

    /* Create new CellBasic clone for this sector Cell */
    CellBasic* sector = clone();

    sector->setNumSectors(0);
    sector->setNumRings(0);

    log_printf(DEBUG, "Creating a new sector Cell with %d for Cell %d",
               sector->getId(), _id);

    /* Add new bounding planar Surfaces to the clone */
    sector->addSurface(+1, planes.at(i));

    if (_num_sectors != 2) {
      if (i+1 < _num_sectors)
        sector->addSurface(-1, planes.at(i+1));
      else
        sector->addSurface(-1, planes.at(0));
    }

    /* Store the clone in the parent Cell's container of sector Cells */
    _sectors.push_back(sector);
  }

  /* Store all of the sectors in the parent Cell's subcells container */
  _subcells.clear();
  _subcells.insert(_subcells.end(), _sectors.begin(), _sectors.end());
}


/**
 * @brief Subdivides the Cell into clones for fuel pin rings.
 */
void CellBasic::ringify() {

  /* If the user didn't request any rings, don't make any */
  if (_num_rings == 0)
        return;

  int num_circles = 0;
  Circle* circle1 = NULL;
  Circle* circle2 = NULL;
  double radius1 = 0;
  double radius2 = 0;
  double x1 = 0.;
  double y1 = 0.;
  double x2 = 0.;
  double y2 = 0.;
  int halfspace1 = 0;
  int halfspace2 = 0;
  std::vector<Circle*> circles;

  /* See if the Cell contains 1 or 2 CIRCLE Surfaces */
  std::map<int, surface_halfspace>::iterator iter1;
  for (iter1=_surfaces.begin(); iter1 != _surfaces.end(); ++iter1) {

    /* Determine if any of the Surfaces is a Circle */
    if (iter1->second._surface->getSurfaceType() == CIRCLE) {
      int halfspace = iter1->second._halfspace;
      Circle* circle = static_cast<Circle*>(iter1->second._surface);

      /* Outermost bounding Circle */
      if (halfspace == -1) {
        halfspace1 = halfspace;
        circle1 = circle;
        radius1 = circle1->getRadius();
        x1 = circle1->getX0();
        y1 = circle1->getY0();
      }

      /* Innermost bounding circle */
      else if (halfspace == +1) {
        halfspace2 = halfspace;
        circle2 = circle;
        radius2 = circle2->getRadius();
        x2 = circle2->getX0();
        y2 = circle2->getY0();
      }

      num_circles++;
    }
  }

  /* Error checking */
  if (num_circles == 0)
    log_printf(ERROR, "Unable to ringify Cell %d since it does not "
              "contain any CIRCLE type Surface(s)", _id);

  if (num_circles > 2)
    log_printf(NORMAL, "Unable to ringify Cell %d since it "
               "contains more than 2 CIRCLE Surfaces", _id);

  if (x1 != x2 && num_circles == 2)
    log_printf(ERROR, "Unable to ringify Cell %d since it contains "
               "Circle %d centered at x=%f and Circle %d at x=%f. "
               "Both Circles must have the same center.",
               _id, circle1->getId(), x1, circle2->getId(), x2);

  if (y1 != y2 && num_circles == 2)
    log_printf(ERROR, "Unable to ringify Cell %d since it contains "
               "Circle %d centered at y=%f and Circle %d at y=%f. "
               "Both Circles must have the same center.",
               _id, circle1->getId(), y1, circle2->getId(), y2);

  if (circle1 == NULL && circle2 != NULL)
    log_printf(ERROR, "Unable to ringify Cell %d since it only contains "
               "the positive halfpsace of Circle %d. Rings can only be "
               "created for Cells on the interior (negative halfspace) "
               "of a CIRCLE Surface.", _id, circle2->getId());

  if (radius1 <= radius2)
    log_printf(ERROR, "Unable to ringify Cell %d since it contains 2 "
               "disjoint CIRCLE Surfaces: halfspace %d for Circle %d "
               "and halfspace %d for Circle %d. Switch the signs of "
               "the 2 halfspaces for each Surface.", _id, halfspace1,
               circle1->getId(), halfspace2, circle2->getId());

  /* Compute the area to fill with each equal volume ring */
  double area = M_PI * fabs(radius1*radius1 - radius2*radius2) / _num_rings;

  /* Generate successively smaller Circle Surfaces */
  for (int i=0; i < _num_rings-1; i++) {
    radius2 = sqrt(radius1*radius1 - (area / M_PI));
    Circle* circle = new Circle(x1, y1, radius1);
    circles.push_back(circle);
    radius1 = radius2;
  }

  /* Store smallest, innermost Circle */
  Circle* circle = new Circle(x1, y1, radius1);
  circles.push_back(circle);

  /* Loop over Circles and create a new Cell clone for each ring */
  std::vector<Circle*>::iterator iter2;
  std::vector<CellBasic*>::iterator iter3;

  for (iter2 = circles.begin(); iter2 != circles.end(); ++iter2) {

    /* Create Circles for each of the sectorized Cells */
    if (_sectors.size() != 0) {
      for (iter3 = _sectors.begin(); iter3 != _sectors.end(); ++iter3) {
        log_printf(DEBUG, "Creating a new ring in sector Cell %d",
                   (*iter3)->getId());

        /* Create a new CellBasic clone */
        CellBasic* ring = (*iter3)->clone();
        ring->setNumSectors(0);
        ring->setNumRings(0);

        /* Add new bounding Circle surfaces to the clone */
        ring->addSurface(-1, (*iter2));

        /* Look ahead and check if we have an inner Circle to add */
        if (iter2+1 == circles.end()) {
          _rings.push_back(ring);
          continue;
        }
        else
          ring->addSurface(+1, *(iter2+1));

        /* Store the clone in the parent Cell's container of ring Cells */
        _rings.push_back(ring);
      }
    }

    /* Create Circles for this un-sectorized Cell */
    else {
      log_printf(DEBUG, "Creating new ring in un-sectorized Cell %d",_id);

      /* Create a new CellBasic clone */
      CellBasic* ring = clone();
      ring->setNumSectors(0);
      ring->setNumRings(0);

      /* Add new bounding Circle Surfaces to the clone */
      ring->addSurface(-1, (*iter2));

      /* Look ahead and check if we have an inner Circle to add */
      if (iter2+1 == circles.end()) {
        _rings.push_back(ring);
        break;
      }
      else
        ring->addSurface(+1, *(iter2+1));

      /* Store the clone in the parent Cell's container of ring Cells */
      _rings.push_back(ring);
    }
  }

  /* Store all of the rings in the parent Cell's subcells container */
  _subcells.clear();
  _subcells.insert(_subcells.end(), _rings.begin(), _rings.end());
}


/**
 * @brief Subdivides a Cell into rings and sectors.
 * @details This method uses the Cell's clone method to produce a vector of
 *          this Cell's subdivided ring and sector Cells.
 * @return a vector of Cell pointers to the new subdivided Cells
 */
std::vector<CellBasic*> CellBasic::subdivideCell() {
  sectorize();
  ringify();
  return _subcells;
}

/**
 * @brief Convert this CellBasic's attributes to a string format.
 * @return a character array of this CellBasic's attributes
 */
std::string CellBasic::toString() {

  std::stringstream string;

  string << "Cell id = " << _id
         << ", type = MATERIAL, material id = " << _material
         << ", universe = " << _universe
         << ", num_surfaces = " << getNumSurfaces()
         << ", num of rings = " << _num_rings
         << ", num of sectors = " << _num_sectors;

  /* Append each of the surface ids to the string */
  std::map<int, surface_halfspace>::iterator iter;
  string << ", surface ids = ";
  for (iter = _surfaces.begin(); iter != _surfaces.end(); ++iter)
    string << iter->first << ", ";

  return string.str();
}


/**
 * @brief Prints a string representation of all of the CellBasic's attributes
 *        to the console.
 */
void CellBasic::printString() {
  log_printf(NORMAL, toString().c_str());
}


/**
 *  @brief CellFill constructor
 *  @param id the user-specified Cell ID
 *  @param universe the ID of the Universe within which this Cell resides
 *  @param universe_fill the ID of the Universe filling this Cell
 */
CellFill::CellFill(int universe, int universe_fill, int id):
  Cell(universe, id) {

  _cell_type = FILL;
  _universe_fill_id = universe_fill;
}


/**
 * @brief Return the ID of the Universe filling this Cell.
 * @return the Universe's id
 */
int CellFill::getUniverseFillId() const {
  return _universe_fill_id;
}


/**
 * @brief Return a pointer to the Universe filling this Cell.
 * @return the universe pointer
 */
Universe* CellFill::getUniverseFill() const {
  return _universe_fill;
}


/**
 * @brief Set a pointer to the Universe filling this CellFill.
 * @param universe the Universe's pointer
 */
void CellFill::setUniverseFillPointer(Universe* universe) {
  _universe_fill = universe;
  _universe_fill_id = universe->getId();
}


/**
 * @brief Convert this CellFill's attributes to a string format.
 * @return a character array of this Cell's attributes
 */
std::string CellFill::toString() {

  std::stringstream string;

  string << "Cell id = " << _id << ", type = FILL, universe_fill = " <<
    _universe_fill_id << ", universe = " << _universe <<
    ", num_surfaces = " << getNumSurfaces();

  /** Add the IDs for the Surfaces in this Cell */
  std::map<int, surface_halfspace>::iterator iter;
  string << ", surface ids = ";
  for (iter = _surfaces.begin(); iter != _surfaces.end(); ++iter)
    string << iter->first << ", ";

  return string.str();
}


/**
 * @brief Prints a string representation of all of the CellFill's attributes
 *        to the console.
 */
void CellFill::printString() {
  log_printf(NORMAL, toString().c_str());
}
