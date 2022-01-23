using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    //everything needed for moving
    public CharacterController controller;
    Vector3 velocity; // x = right left, z = forward backward, y = up down
    Vector3 move;
    public float speed = 12f;
    public float gravity = -9.81f;
    public float movementSmoothness = 5f;
    public float verticalSpeed = 3f;
    public float rayLenght = 8f;

    //ground check stuff
    public Transform groundCheck;
    public float groundDistance = 0.4f;
    public LayerMask groundMask;

    // Update is called once per frame
    void Update()
    {

        //isGrounded = Physics.CheckSphere(groundCheck.position, groundDistance, groundMask); //creates sphere with radius(Distance), and checks if anything collides with it.
        float x = getForward();
        float z = getSideways();

        move = transform.right * x + transform.forward * z;//movement based on player facing and x and z;

        Ray downRay = new Ray(controller.transform.position, -controller.transform.up);
        RaycastHit hitDown;

        if (Input.GetKey(KeyCode.Space))
        {
            velocity.y = verticalSpeed; //fly up
        }
        if (Input.GetKey(KeyCode.LeftControl))
        {
            Debug.DrawRay(controller.transform.position, -controller.transform.up * 1f, Color.blue);
            if (Physics.Raycast(downRay, out hitDown, 1f) && !hitDown.collider.isTrigger)
            {
                velocity.y = 0;
            }
            else
            {
                velocity.y = -verticalSpeed; //fly down
            }
        }
        move = Vector3.Lerp(controller.transform.position, move, movementSmoothness); // smooth everything out 
        controller.Move(move * Time.deltaTime); // move * speed * deltaTime -> to make it independent from framerate
        controller.Move(velocity * Time.deltaTime); // t^2 (time * time)
        velocity = Vector3.zero;
    }

    float getForward()
    {
        float x = Input.GetAxis("Horizontal") * 0.5f * speed; // left right
        if (x > 0)
        {
            Ray horizontalRay = new Ray(controller.transform.position, controller.transform.right);
            Debug.DrawRay(controller.transform.position, controller.transform.right * rayLenght, Color.green);
            RaycastHit hit;
            if (Physics.Raycast(horizontalRay, out hit, rayLenght) && !hit.collider.isTrigger)
            {
                x = 0;
            }
        }
        else
        {
            Ray horizontalRay = new Ray(controller.transform.position, -controller.transform.right);
            Debug.DrawRay(controller.transform.position, -controller.transform.right * rayLenght, Color.green);
            RaycastHit hit;
            if (Physics.Raycast(horizontalRay, out hit, rayLenght) && !hit.collider.isTrigger)
            {
                x = 0;
            }
        }
        return x;
    }

    float getSideways()
    {
        float z = Input.GetAxis("Vertical") *  speed; //forward backward
        if (z > 0)
        {
            Ray horizontalRay = new Ray(controller.transform.position, controller.transform.forward);
            Debug.DrawRay(controller.transform.position, controller.transform.forward * rayLenght, Color.red);
            RaycastHit hit;
            if (Physics.Raycast(horizontalRay, out hit, rayLenght) && !hit.collider.isTrigger)
            {
                z = 0;
            }
        }
        else
        {
            Ray horizontalRay = new Ray(controller.transform.position, -controller.transform.forward);
            Debug.DrawRay(controller.transform.position, -controller.transform.forward * rayLenght, Color.red);
            RaycastHit hit;
            if (Physics.Raycast(horizontalRay, out hit, rayLenght) && !hit.collider.isTrigger)
            {
                z = 0;
            }
        }
        return z;
    }
}
