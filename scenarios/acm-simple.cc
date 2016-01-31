#include <ns3/core-module.h>
#include <ns3/network-module.h>
#include <ns3/ndnSIM-module.h>

namespace ns3 {
int
main(int argc, char* argv[])
{
  CommandLine cmd;
  cmd.Parse(argc, argv);

  AnnotatedTopologyReader topologyReader("", 1.0);
  topologyReader.SetFileName("topologies/topo-2node-loss.txt");
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
  std::string prefix = "/prefix";


  ndn::AppHelper consumerHelper("ns3::ndn::ConsumerCbr");
  consumerHelper.SetPrefix(prefix);
  consumerHelper.SetAttribute("Frequency", StringValue("100")); // 100 interests a second
  consumerHelper.Install(consumerNodes);

  int stage = 10;
  for (int i=0; i < stage; i++) {
      ndn::AppHelper producerHelper("ns3::ndn::Producer");
      producerHelper.SetPrefix(prefix);
      // producerHelper.SetAttribute("PayloadSize", StringValue(to_string(1475+i*1500)));
      producerHelper.SetAttribute("PayloadSize", StringValue("8000"));
      ApplicationContainer apps = producerHelper.Install(producer);
      apps.Start(Seconds(20.0*i));
      apps.Stop(Seconds(20.0*i + 20.0));
  }



  // Add /prefix origins to ndn::GlobalRouter
  ndnGlobalRoutingHelper.AddOrigins(prefix, producer);

  // Calculate and install FIBs
  ndn::GlobalRoutingHelper::CalculateRoutes();

  // Simulator::Stop(Seconds(20.0*stage));
  Simulator::Stop(Seconds(80));
  // L2RateTracer::InstallAll("results/l2rate-trace.txt", Seconds(0.5));
  // ndn::L3RateTracer::InstallAll("results/l3rate-trace.txt", Seconds(1.0));


  Simulator::Run();
  Simulator::Destroy();
  std::cout << "end" << std::endl;

  return 0;
}
} // namespace ns3

int
main(int argc, char* argv[])
{
  return ns3::main(argc, argv);
}
