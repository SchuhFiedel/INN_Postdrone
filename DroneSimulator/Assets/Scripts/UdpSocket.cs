/*
Created by Youssef Elashry to allow two-way communication between Python3 and Unity to send and receive strings

Feel free to use this in your individual or commercial projects BUT make sure to reference me as: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry
It would be appreciated if you send me how you have used this in your projects (e.g. Machine Learning) at youssef.elashry@gmail.com

Use at your own risk
Use under the Apache License 2.0

Modified by: 
Youssef Elashry 12/2020 (replaced obsolete functions and improved further - works with Python as well)
Based on older work by Sandra Fang 2016 - Unity3D to MATLAB UDP communication - [url]http://msdn.microsoft.com/de-de/library/bb979228.aspx#ID0E3BAC[/url]
*/

using UnityEngine;
using System.Collections;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Globalization;

public class UdpSocket : MonoBehaviour
{
    [HideInInspector] public bool isTxStarted = false;

    [SerializeField] string IP = "127.0.0.1"; // local host
    [SerializeField] int rxPort = 8000; // port to receive data from Python on
    [SerializeField] int txPort = 8001; // port to send data to Python on

    int i = 0; // DELETE THIS: Added to show sending data from Unity to Python via UDP

    // Create necessary UdpClient objects
    UdpClient client;
    IPEndPoint remoteEndPoint;
    Thread receiveThread; // Receiving Thread

    PythonMovement pyMove;
    public GameObject player;
    private float receivedAngle = 0;
    private float receivedHeight = 0;

    IEnumerator SendDataCoroutine() // DELETE THIS: Added to show sending data from Unity to Python via UDP
    {
        while (true)
        {
            SendData("Sent from Unity: " + i.ToString());
            i++;
            yield return new WaitForSeconds(1f);
        }
    }

    public void SendData(string message) // Use to send data to Python
    {
        //Debug.Log("DD");
        try
        {
            //Debug.Log("MESSAGE: "+ message);
            byte[] data = Encoding.UTF8.GetBytes(message);
            client.Send(data, data.Length, remoteEndPoint);
        }
        catch (Exception err)
        {
            print(err.ToString());
        }
    }

    private void  ReceiveData()
    {
        //Debug.Log("CC");
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = client.Receive(ref anyIP);
                string text = Encoding.UTF8.GetString(data);
                //Debug.Log("RECEIVED MESSAGE>> " + text);
                string[] msgs = text.Split(',');
                receivedAngle = float.Parse(msgs[0], CultureInfo.InvariantCulture);
                //receivedHeight = float.Parse(msgs[1], CultureInfo.InvariantCulture);
                //Debug.Log(receivedAngle);
                //Debug.Log(receivedHeight);
            }
            catch (Exception err)
            {
                print(err.ToString());
            }
        }
    }


    private void Start()
    {
        pyMove = player.GetComponent<PythonMovement>();

        // Create remote endpoint (to Matlab) 
        remoteEndPoint = new IPEndPoint(IPAddress.Parse(IP), txPort);
        //Debug.Log("AA");
        // Create local client
        client = new UdpClient(rxPort);
        //Debug.Log("BB");
        // local endpoint define (where messages are received)
        // Create a new thread for reception of incoming messages
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();

        // Initialize (seen in comments window)
        Debug.Log("UDP Comms Initialised");

        //StartCoroutine(SendDataCoroutine()); // DELETE THIS: Added to show sending data from Unity to Python via UDP
    }

    private void Update()
    {
        Debug.Log("AYE: "+ receivedAngle + ";;" + receivedHeight);
        float[] playerPosition = pyMove.Movement(receivedAngle, receivedHeight);

        //Debug.Log("PLAYER POS " + playerPosition[0] + " " +playerPosition[1]);

        string message = playerPosition[0].ToString().Replace(",",".") + ", " + playerPosition[1].ToString().Replace(",", ".") + ", " + playerPosition[2].ToString().Replace(",", ".");

        SendData(message);
    }

    //Prevent crashes - close clients and threads properly!
    void OnDisable()
    {
        if (receiveThread != null)
            receiveThread.Abort();

        client.Close();
    }
}