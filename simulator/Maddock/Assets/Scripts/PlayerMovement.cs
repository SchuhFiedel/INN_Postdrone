using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;
using System.IO.Pipes;

public class PlayerMovement : MonoBehaviour
{
    //everything needed for moving
  
    public CharacterController controller;
    Vector3 move;
    public float speed = 12f;

    Vector3 velocity; // x = right left, z = forward backward, y = up down
    public float gravity = -9.81f;

    //ground check stuff
    public Transform groundCheck;
    public float groundDistance = 0.4f;
    public LayerMask groundMask;
    private bool isGrounded;

    //jumpstuff
    public float jumpHeight = 3f;

    //Rotation
    private bool _rotate;

    //Writing and Reading
    public StreamWriter sw;
    public StreamReader sr;
    public NamedPipeServerStream pipe_out;
    public NamedPipeClientStream pipe_in;


    // Update is called once per frame

    void Awake()
    {
        
          
            Debug.Log("Awoken");
        string path_w = @"E:\Programming\Python\Postdrone\GPS_Rotation.txt";
        // string path_r = @"E:\Programming\Python\Postdrone\GPS_Rotation.txt";
        try 
        {
            this.pipe_out = new NamedPipeServerStream("out", PipeDirection.Out);
            this.pipe_in = new NamedPipeClientStream(".", "in", PipeDirection.In);




            this.sr = new StreamReader(pipe_in);
            this.sw = new StreamWriter(pipe_out);
                
        
        }
        catch(Exception e)
        {
            Debug.Log(e);
            
        }

    }

    void Update()
    {
        isGrounded = Physics.CheckSphere(groundCheck.position, groundDistance, groundMask); //creates sphere with radius(Distance), and checks if anything collides with it.
        float x = Input.GetAxis("Horizontal") * speed;
        float z = Input.GetAxis("Vertical")   * speed;


        if (_rotate)
        {
            transform.Rotate(new Vector3(0, 1, 0));
        }

        if (Input.GetKey(KeyCode.T) == true)
        {
            OnPress();
        }
        else
        {
            OnRelease();
        }

        if (velocity.y < 0)
        {
            velocity.y = -2f; //small number because it will trigger before we are on the ground and we want to keep the player on the ground
        }
      //  Debug.Log(gameObject.transform.rotation.y);
        move = transform.right * x + transform.forward * z ;//movement based on player facing and x and z;
        //Write_GPS(gameObject.transform.rotation.y);
        if (Input.GetButtonDown("Jump") /*&& isGrounded*/) {

            velocity.y = Mathf.Sqrt(jumpHeight * -2 * gravity); //jump velocity = sqr(desired Height * -2 * gravity)
        }

        velocity.y += gravity * Time.deltaTime; //calculate falling velocity
        controller.Move(move * Time.deltaTime); // move * speed * deltaTime -> to make it independent from framerate
        controller.Move(velocity * Time.deltaTime); // t^2 (time * time)

    }

    void OnPress()
    {
        _rotate = true;
    }

    void OnRelease()
    {
        _rotate = false;
    }

    void Write_GPS(float postition)
    {  
        sw.WriteLine(postition.ToString());
    }


    public void Dispose()
    {
        sw.Dispose();
    }
}
