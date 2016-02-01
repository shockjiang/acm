#include <ns3/core-module.h>
#include <ns3/network-module.h>
#include <ns3/ndnSIM-module.h>

namespace ns3 {
int
main(int argc, char* argv[])
{
  int stage = 17; 
  float interval = 20.0;
  string topo = "topologies/topo-3link-loss1.txt";
  int loss = 1;
  int load = 50;
  string id = "2";
  CommandLine cmd;
  cmd.AddValue("loss", "frame loss rate ratio (x100)", loss);
  cmd.AddValue("topo", "topology input file", topo);
  cmd.AddValue("id", "id of the running instance", id);
  cmd.AddValue("load", "load of one way, 100 in total", load);
  cmd.Parse(argc, argv);
  
  string suffix = "-loss" + to_string(loss) +"-load" + to_string(load)
                 + "-id" + id;
  AnnotatedTopologyReader topologyReader("", 1.0);
  topologyReader.SetFileName(topo);
  topologyReader.Read();

  // Install NDN stack on all nodes
  ndn::StackHelper ndnHelper;
  ndnHelper.InstallAll();

  ndn::StrategyChoiceHelper::InstallAll("/", "ndn:/localhost/nfd/strategy/best-route");

  // Installing global routing interface on all nodes
  ndn::GlobalRoutingHelper ndnGlobalRoutingHelper;
  ndnGlobalRoutingHelper.InstallAll();

  // Getting containers for the consumer/producer
  Ptr<Node> producer = Names::Find<Node>("Node1");
  NodeContainer consumerNodes;
  consumerNodes.Add(Names::Find<Node>("Node0"));

  // Install NDN applications
  std::string prefixA = "/prefix/A";
  std::string prefixB = "/prefix/B";

  for (int i = 0; i < stage; i++) {
    ndn::AppHelper consumerHelper("ns3::ndn::ConsumerCbr");
    consumerHelper.SetPrefix(prefixA + "/" + to_string(625 + i * 500));
    consumerHelper.SetAttribute("Frequency", StringValue(to_string(load))); // 100 interests a second
    ApplicationContainer apps = consumerHelper.Install(consumerNodes);
    apps.Start(Seconds(interval * i));
    apps.Stop(Seconds(interval * i + interval));
  }

for (int i = 0; i < stage; i++) {
    ndn::AppHelper consumerHelper("ns3::ndn::ConsumerCbr");
    consumerHelper.SetPrefix(prefixB + "/" + to_string(625 + i * 500));
    consumerHelper.SetAttribute("Frequency", StringValue(to_string(100-load))); // 100 interests a second
    ApplicationContainer apps = consumerHelper.Install(consumerNodes);
    apps.Start(Seconds(interval * i));
    apps.Stop(Seconds(interval * i + interval));
  }

  ndn::AppHelper producerHelper("ns3::ndn::ProducerACM");
  producerHelper.SetPrefix(prefixA);
  producerHelper.SetAttribute("PayloadSize", StringValue("1024"));
  ApplicationContainer apps = producerHelper.Install(producer);
  apps.Start(Seconds(0));

  ndn::AppHelper producerHelper2("ns3::ndn::ProducerACM");
  producerHelper2.SetPrefix(prefixB);
  producerHelper2.SetAttribute("PayloadSize", StringValue("1024"));
  ApplicationContainer apps2 = producerHelper2.Install(producer);
  apps2.Start(Seconds(0));

  ndn::FibHelper::AddRoute("Node0", prefixA, "Node1", 1); // link 257, 
  ndn::FibHelper::AddRoute("Node0", prefixB, "Node2", 1); // link 256, two links
  ndn::FibHelper::AddRoute("Node2", prefixB, "Node1", 1); 


  Simulator::Stop(Seconds(interval*stage + 1));

//  L2RateTracer::InstallAll("results/l2rate-trace.txt", Seconds(0.5));
  ndn::L3RateTracer::InstallAll("results/l3rate-trace"+suffix+".txt", Seconds(1.0));

  Simulator::Run();
  Simulator::Destroy();
  std::cout << "end: suffix=" << suffix << ". topo: " << topo << std::endl;

  return 0;
}
} // namespace ns3

int
main(int argc, char* argv[])
{
  return ns3::main(argc, argv);
}
