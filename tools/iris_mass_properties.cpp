// Parse a Stonefish scenario headless (no ROS, no GPU) and print the mass properties of every
// robot link: CG and CB in the link origin frame, principal inertia, and each compound part.
// Scenario includes must be plain paths: $(find ...) is resolved by stonefish_ros2, not here.
#include <Stonefish/core/ConsoleSimulationApp.h>
#include <Stonefish/core/SimulationManager.h>
#include <Stonefish/core/ScenarioParser.h>
#include <Stonefish/core/Robot.h>
#include <Stonefish/entities/SolidEntity.h>
#include <Stonefish/entities/solids/Compound.h>
#include <cstdio>
#include <cstdlib>
#include <string>

class Mgr : public sf::SimulationManager
{
public:
    explicit Mgr(std::string f) : sf::SimulationManager(100.0), file(std::move(f)) {}
    void BuildScenario() override
    {
        sf::ScenarioParser p(this);
        if (!p.Parse(file)) { fprintf(stderr, "PARSE FAILED\n"); exit(2); }
    }
    std::string file;
};

class App : public sf::ConsoleSimulationApp
{
public:
    using sf::ConsoleSimulationApp::ConsoleSimulationApp;
    using sf::ConsoleSimulationApp::Init;
};

static void printT(const char* label, const sf::Transform& T)
{
    sf::Scalar y, p, r;
    T.getBasis().getEulerYPR(y, p, r);
    const sf::Vector3 o = T.getOrigin();
    printf("  %-28s xyz=(%+.4f, %+.4f, %+.4f) rpy=(%+.3f, %+.3f, %+.3f)\n", label, o.x(), o.y(), o.z(), r, p, y);
}

int main(int argc, char** argv)
{
    if (argc < 3) { fprintf(stderr, "usage: cgtool <data dir> <scenario.scn> [nparts]\n"); return 1; }
    const int nparts = argc > 3 ? atoi(argv[3]) : 0;
    setvbuf(stdout, nullptr, _IONBF, 0);
    Mgr* m = new Mgr(argv[2]);
    App app("cgtool", argv[1], m);
    app.Init();

    for (unsigned int ri = 0;; ++ri)
    {
        sf::Robot* rob = nullptr;
        try { rob = m->getRobot(ri); } catch (...) { break; }
        if (rob == nullptr) break;
        for (size_t li = 0;; ++li)
        {
            sf::SolidEntity* link = nullptr;
            try { link = rob->getLink(li); } catch (...) { break; }
            if (link == nullptr) break;
            printf("\n== robot '%s' link '%s': mass %.3f kg, volume %.1f cm3\n", rob->getName().c_str(),
                   link->getName().c_str(), link->getMass(), link->getVolume() * 1e6);
            const sf::Transform cg2o = link->getCG2OTransform();
            printT("T_CG2O", cg2o);
            printT("T_CG2O^-1 (CG pose in O)", cg2o.inverse());
            const sf::Vector3 cb_cg = link->getCB();
            const sf::Vector3 cb_o = cg2o.inverse() * cb_cg;
            printf("  %-28s (%+.4f, %+.4f, %+.4f)\n", "CB in CG frame", cb_cg.x(), cb_cg.y(), cb_cg.z());
            printf("  %-28s (%+.4f, %+.4f, %+.4f)\n", "CB in O frame", cb_o.x(), cb_o.y(), cb_o.z());
            const sf::Vector3 I = link->getInertia();
            printf("  %-28s (%.3f, %.3f, %.3f)\n", "principal inertia", I.x(), I.y(), I.z());

            sf::Compound* comp = dynamic_cast<sf::Compound*>(link);
            if (comp != nullptr && nparts > 0)
            {
                printf("  parts (CG of each part in link O frame):\n");
                for (int i = 0; i < nparts; ++i)
                {
                    sf::CompoundPart part;
                    try { part = comp->getPart(i); } catch (...) { break; }
                    if (part.solid == nullptr) break;
                    const sf::Vector3 pcg = (part.origin * part.solid->getCG2OTransform().inverse()).getOrigin();
                    sf::Scalar y, p, r; part.origin.getBasis().getEulerYPR(y, p, r);
                    printf("   %-20s %s m=%6.3f V=%8.1f cm3 buoyant=%d  cg=(%+.4f,%+.4f,%+.4f) origin_yaw=%+.3f\n",
                           part.solid->getName().c_str(), part.isExternal ? "ext" : "int",
                           part.solid->getMass(), part.solid->getVolume() * 1e6, (int)part.solid->isBuoyant(),
                           pcg.x(), pcg.y(), pcg.z(), y);
                }
            }
        }
    }
    return 0;
}
