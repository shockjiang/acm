#include <ns3/core-module.h>
#include <ns3/network-module.h>
#include <ns3/ndnSIM-module.h>

namespace ns3 {
int
main(int argc, char* argv[])
{
  int stage = 17; 
  float interval = 20.0;
  string topo = "topologies/topo-3node-loss10.txt";
  int loss = 0;
  string id = "x";
  CommandLine cmd;
  cmd.AddValue("loss", "frame loss rate ratio (x100)", loss);
  cmd.AddValue("topo", "topology input file", topo);
  cmd.AddValue("id", "id of the running instance", id);

  cmd.Parse(argc, argv);
  
  string suffix = "-loss" + to_string(loss) + "-id" + id;
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
  std::string prefix = "/prefix";


//  ndn::AppHelper consumerHelper("ns3::ndn::ConsumerCbr");
//  consumerHelper.SetPrefix(prefix);
//  consumerHelper.SetAttribute("Frequency", StringValue("100")); // 100 interests a second
//  consumerHelper.Install(consumerNodes);
//


  for (int i = 0; i < stage; i++) {
    ndn::AppHelper consumerHelper("ns3::ndn::ConsumerCbr");
    consumerHelper.SetPrefix(prefix + "/" + to_string(625 + i * 500));
    consumerHelper.SetAttribute("Frequency", StringValue("100")); // 100 interests a second
    ApplicationContainer apps = consumerHelper.Install(consumerNodes);
    apps.Start(Seconds(interval * i));
    apps.Stop(Seconds(interval * i + interval));
  }


//  for (int i=0; i < stage; i++) {
//      ndn::AppHelper producerHelper("ns3::ndn::Producer");
//      producerHelper.SetPrefix(prefix);
//      producerHelper.SetAttribute("PayloadSize", StringValue(to_string(1475+i*1500)));
//      // producerHelper.SetAttribute("PayloadSize", StringValue("16475"));
//      ApplicationContainer apps = producerHelper.Install(producer);
//      apps.Start(Seconds(interval*i));
//      apps.Stop(Seconds(interval*i + interval));
//  }
//

    ndn::AppHelper producerHelper("ns3::ndn::ProducerACM");
    producerHelper.SetPrefix(prefix);
    producerHelper.SetAttribute("PayloadSize", StringValue("1024"));
    ApplicationContainer apps = producerHelper.Install(producer);
    apps.Start(Seconds(0));

  // Add /prefix origins to ndn::GlobalRouter
  ndnGlobalRoutingHelper.AddOrigins(prefix, producer);

  // Calculate and install FIBs
  ndn::GlobalRoutingHelper::CalculateRoutes();

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
