/* -*-  Mode: C++; c-file-style: "gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2013 University of California, Los Angeles
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * Author: Alexander Afanasyev <alexander.afanasyev@ucla.edu>
 */

#include <ns3/core-module.h>

#include <ns3/ndnSIM-module.h>
#include <ns3/ndnSIM/utils/tracers/ndn-l3-rate-tracer.h>
#include <ns3/ndnSIM/apps/ndn-consumer-cbr.h>

#include <vector>

using namespace std;
using namespace boost;
using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("Experiment.select.ns");

#define _LOG_INFO(x) NS_LOG_INFO(x)


int
main (int argc, char *argv[])
{
  LogComponentEnable ("ndn.ConsumerCbr", LOG_LEVEL_INFO);
  LogComponentEnable ("Experiment.select.ns", LOG_LEVEL_INFO);

  CommandLine cmd;
  cmd.Parse (argc, argv);

  string prefix = "/prefix";

  AnnotatedTopologyReader topologyReader ("", 1);
  topologyReader.SetFileName ("topologies/ndns-5node.txt");
  topologyReader.Read ();

  NodeContainer consumers = {(Ptr<Node>)Names::Find<Node>("0")};
  NodeContainer producers = {(Ptr<Node>)Names::Find<Node>("2"),
                             (Ptr<Node>)Names::Find<Node>("3"),
                             (Ptr<Node>)Names::Find<Node>("4")};

  NodeContainer routers = {Names::Find<Node>("1")};

  // Install NDN stack on all nodes
  ndn::StackHelper ndnHelper;
  //ndnHelper.SetForwardingStrategy ("ns3::ndn::fw::BestRoute");
  // ndnHelper.SetForwardingStrategy ("ns3::ndn::fw::SmartFlooding");

//  ndnHelper.SetForwardingStrategy ("ns3::ndn::fw::BestRoute::PerOutFaceLimits"
//                                   "Limit", "ns3::ndn::Limits::Window");
  ndnHelper.SetForwardingStrategy ("ns3::ndn::fw::BestRoute");
  ndnHelper.SetForwardingStrategy ("ns3::ndn::fw::BestRoute::PerOutFaceLimits",
                                   "Limit", "ns3::ndn::Limits::Rate",
                                   "EnableNACKs", "true");
  ndnHelper.EnableLimits (true);
  //ndnHelper.EnableLimits (true, Seconds (0.3), 40, 1040);
  ndnHelper.SetDefaultRoutes (false);
  ndnHelper.InstallAll ();
  //ndnHelper.Install(routers);

  ndn::GlobalRoutingHelper ndnGlobalRoutingHelper;
  ndnGlobalRoutingHelper.InstallAll ();

  int START_FREQ = 400;
  int INTERVAL = 10.0;
  int STAGE_CNT = 8;
  string suffix;
  suffix += "-freq"+to_string(START_FREQ)+"-intv" + to_string(INTERVAL) + "-stg" + to_string(STAGE_CNT);

  std::cout <<"Simulation begins, parameters: " << suffix << std::endl;

  // Consumer
  ndn::AppHelper consumerHelper ("ns3::ndn::ConsumerCbr");
  consumerHelper.SetPrefix (prefix +"/c0");
  consumerHelper.SetAttribute ("Frequency", StringValue (to_string(START_FREQ)));
  ApplicationContainer apps = consumerHelper.Install (consumers);
  apps.Start(Seconds(0.0));


  for (int i=1; i <= STAGE_CNT; i++) {
    ndn::AppHelper consumerHelper ("ns3::ndn::ConsumerCbr");
    consumerHelper.SetPrefix (prefix +"/c" + to_string(i));
    consumerHelper.SetAttribute ("Frequency", StringValue ("100"));
    ApplicationContainer apps = consumerHelper.Install (consumers);
    apps.Start(Seconds(INTERVAL * i));
  }
  // Simulator::Schedule (Seconds (40.0), ndn::LinkControlHelper::FailLink, Names::Find<Node>("1"), Names::Find<Node>("4"));

  // Producer
  ndn::AppHelper producerHelper ("ns3::ndn::Producer");
  producerHelper.SetPrefix (prefix);
  producerHelper.SetAttribute ("PayloadSize", StringValue("1000"));
  producerHelper.Install (producers); // last node

  // Add /prefix origins to ndn::GlobalRouter
  //  ndnGlobalRoutingHelper.AddOrigins (prefix, producers);
  //  ndn::GlobalRoutingHelper::CalculateRoutes ();

  // Manually configure FIB routes
  ndn::StackHelper::AddRoute  ("0", prefix, "1", 1); // link to n1
  ndn::StackHelper::AddRoute  ("1", prefix, "2", 1); // link to n1
  ndn::StackHelper::AddRoute  ("1", prefix, "3", 5); // link to n1
  ndn::StackHelper::AddRoute  ("1", prefix, "4", 10); // link to n1


  ndn::AppDelayTracer::Install(consumers, "results/delay-trace" + suffix + ".txt");
  ndn::L3AggregateTracer::Install(routers, "results/aggregate-trace" + suffix + ".txt", Seconds (1.0));

  Simulator::Stop (Seconds((STAGE_CNT + 1) * INTERVAL + 1.0));
  Simulator::Run ();


  std::cout <<"end" << std::endl;
  Simulator::Destroy ();
  return 0;
}
